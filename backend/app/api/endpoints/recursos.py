# backend/app/api/endpoints/recursos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional

from app.api import deps
from app.crud import crud_recurso, crud_recurso_concepto
from app.schemas.recurso import Recurso, RecursoCreate, RecursoUpdate, RecursoWithConcepts
from app.schemas.recurso_concepto import RecursoConceptosCreate
from app.models.user import User as UserModel
from app.models.user import UserRole

router = APIRouter()

# ----------------- Endpoint para OBTENER todos los recursos -----------------
@router.get("/", response_model=List[Recurso])
async def read_recursos(
    skip: int = 0,
    limit: int = 100,
    tipo: Optional[str] = None,
    nivel_dificultad: Optional[str] = None,
    solo_activos: bool = True,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene una lista de todos los recursos.
    - Administradores: Ven todos los recursos
    - Docentes: Solo ven recursos asociados a conceptos de categorías relacionadas con sus cursos
    - Estudiantes: Ven todos los recursos activos
    Filtros opcionales: tipo, nivel_dificultad
    """
    from app.crud import crud_concepto
    
    # Si el usuario es docente, filtrar por categorías de conceptos de sus cursos
    if current_user.rol == UserRole.DOCENTE:
        categorias_profesor = crud_concepto.get_categorias_conceptos_by_teacher_courses(
            db, teacher_id=current_user.id
        )
        
        # Si el docente tiene cursos con conceptos asociados, filtrar
        if categorias_profesor:
            # Obtener recursos filtrados por categorías
            recursos = crud_recurso.get_recursos_by_categorias_conceptos(
                db, categorias=categorias_profesor, skip=skip, limit=limit, solo_activos=solo_activos
            )
            
            # Aplicar filtros adicionales si se especifican
            if tipo:
                recursos = [r for r in recursos if r.tipo == tipo]
            if nivel_dificultad:
                recursos = [r for r in recursos if r.nivel_dificultad == nivel_dificultad]
        else:
            # Si el docente no tiene cursos con conceptos, retornar lista vacía
            return []
    else:
        # Para administradores y estudiantes: comportamiento normal
        if tipo:
            recursos = crud_recurso.get_recursos_by_tipo(db, tipo=tipo, skip=skip, limit=limit, solo_activos=solo_activos)
        elif nivel_dificultad:
            recursos = crud_recurso.get_recursos_by_nivel_dificultad(db, nivel=nivel_dificultad, skip=skip, limit=limit, solo_activos=solo_activos)
        else:
            recursos = crud_recurso.get_recursos(db, skip=skip, limit=limit, solo_activos=solo_activos)
    
    return recursos

# ----------------- Endpoint para OBTENER un recurso por ID -----------------
@router.get("/{recurso_id}", response_model=Recurso)
async def read_recurso_by_id(
    recurso_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene un recurso específico por su ID.
    Acceso: Cualquier usuario autenticado.
    """
    recurso = crud_recurso.get_recurso_by_id(db, recurso_id=recurso_id)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    return recurso

# ----------------- Endpoint para CREAR un recurso -----------------
@router.post("/", response_model=Recurso, status_code=status.HTTP_201_CREATED)
async def create_recurso(
    recurso_in: RecursoCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Crea un nuevo recurso.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden crear recursos"
        )
    
    recurso = crud_recurso.create_recurso(db, recurso_in=recurso_in)
    return recurso

# ----------------- Endpoint para CREAR un recurso con conceptos -----------------
@router.post("/with-concepts", response_model=RecursoWithConcepts, status_code=status.HTTP_201_CREATED)
async def create_recurso_with_concepts(
    recurso_in: RecursoCreate,
    conceptos_in: RecursoConceptosCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Crea un nuevo recurso y asocia conceptos en una sola operación.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden crear recursos"
        )
    
    # Crear el recurso
    recurso = crud_recurso.create_recurso(db, recurso_in=recurso_in)
    
    # Asociar conceptos
    if conceptos_in.concepto_ids:
        crud_recurso_concepto.associate_conceptos_to_recurso(
            db,
            recurso_id=recurso.id,
            concepto_ids=conceptos_in.concepto_ids,
            relevancias=conceptos_in.relevancias
        )
    
    # Recargar con conceptos
    db.refresh(recurso)
    return recurso

# ----------------- Endpoint para ACTUALIZAR un recurso -----------------
@router.put("/{recurso_id}", response_model=Recurso)
async def update_recurso(
    recurso_id: int,
    recurso_in: RecursoUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Actualiza un recurso existente.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden actualizar recursos"
        )
    
    db_recurso = crud_recurso.get_recurso_by_id(db, recurso_id=recurso_id)
    if not db_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    recurso = crud_recurso.update_recurso(db, db_recurso=db_recurso, recurso_in=recurso_in)
    return recurso

# ----------------- Endpoint para ELIMINAR un recurso -----------------
@router.delete("/{recurso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recurso(
    recurso_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Elimina un recurso.
    Acceso: Solo administradores.
    """
    if current_user.rol != UserRole.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar recursos"
        )
    
    db_recurso = crud_recurso.get_recurso_by_id(db, recurso_id=recurso_id)
    if not db_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    crud_recurso.delete_recurso(db, recurso_id=recurso_id)
    return None

# ----------------- Endpoint para ACTIVAR/DESACTIVAR un recurso -----------------
@router.patch("/{recurso_id}/toggle-activo", response_model=Recurso)
async def toggle_recurso_activo(
    recurso_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Activa o desactiva un recurso (soft delete).
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden activar/desactivar recursos"
        )
    
    recurso = crud_recurso.toggle_recurso_activo(db, recurso_id=recurso_id)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    return recurso

# ----------------- Endpoint para ASOCIAR conceptos a un recurso -----------------
@router.post("/{recurso_id}/conceptos", response_model=List[Any])
async def associate_conceptos_to_recurso(
    recurso_id: int,
    conceptos_in: RecursoConceptosCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Asocia múltiples conceptos a un recurso.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden asociar conceptos a recursos"
        )
    
    # Verificar que el recurso existe
    recurso = crud_recurso.get_recurso_by_id(db, recurso_id=recurso_id)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    relaciones = crud_recurso_concepto.associate_conceptos_to_recurso(
        db,
        recurso_id=recurso_id,
        concepto_ids=conceptos_in.concepto_ids,
        relevancias=conceptos_in.relevancias
    )
    
    return relaciones

