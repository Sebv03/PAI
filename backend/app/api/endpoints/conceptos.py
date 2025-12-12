# backend/app/api/endpoints/conceptos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.crud import crud_concepto
from app.schemas.concepto import Concepto, ConceptoCreate, ConceptoUpdate
from app.models.user import User as UserModel
from app.models.user import UserRole

router = APIRouter()

# ----------------- Endpoint para OBTENER todos los conceptos -----------------
@router.get("/", response_model=List[Concepto])
async def read_conceptos(
    skip: int = 0,
    limit: int = 100,
    categoria: str = None,
    nivel: str = None,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene una lista de todos los conceptos.
    - Administradores: Ven todos los conceptos
    - Docentes: Solo ven conceptos de categorías relacionadas con sus cursos
    - Estudiantes: Ven todos los conceptos
    Filtros opcionales: categoria, nivel
    """
    # Si el usuario es docente, filtrar por categorías de sus cursos
    if current_user.rol == UserRole.DOCENTE:
        categorias_profesor = crud_concepto.get_categorias_conceptos_by_teacher_courses(
            db, teacher_id=current_user.id
        )
        
        # Si el docente tiene cursos con conceptos asociados, filtrar
        if categorias_profesor:
            if categoria:
                # Si se especifica una categoría, verificar que esté en las categorías del profesor
                if categoria not in categorias_profesor:
                    return []  # No tiene acceso a esta categoría
                conceptos = crud_concepto.get_conceptos_by_categoria(db, categoria=categoria, skip=skip, limit=limit)
            elif nivel:
                # Filtrar por nivel pero solo dentro de las categorías del profesor
                conceptos = crud_concepto.get_conceptos_by_categorias(db, categorias=categorias_profesor, skip=skip, limit=limit)
                # Filtrar por nivel adicionalmente
                conceptos = [c for c in conceptos if c.nivel == nivel]
            else:
                # Mostrar solo conceptos de las categorías del profesor
                conceptos = crud_concepto.get_conceptos_by_categorias(db, categorias=categorias_profesor, skip=skip, limit=limit)
        else:
            # Si el docente no tiene cursos con conceptos, retornar lista vacía
            return []
    else:
        # Para administradores y estudiantes: comportamiento normal
        if categoria:
            conceptos = crud_concepto.get_conceptos_by_categoria(db, categoria=categoria, skip=skip, limit=limit)
        elif nivel:
            conceptos = crud_concepto.get_conceptos_by_nivel(db, nivel=nivel, skip=skip, limit=limit)
        else:
            conceptos = crud_concepto.get_conceptos(db, skip=skip, limit=limit)
    
    return conceptos

# ----------------- Endpoint para OBTENER un concepto por ID -----------------
@router.get("/{concepto_id}", response_model=Concepto)
async def read_concepto_by_id(
    concepto_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene un concepto específico por su ID.
    Acceso: Cualquier usuario autenticado.
    """
    concepto = crud_concepto.get_concepto_by_id(db, concepto_id=concepto_id)
    if not concepto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concepto no encontrado"
        )
    return concepto

# ----------------- Endpoint para CREAR un concepto -----------------
@router.post("/", response_model=Concepto, status_code=status.HTTP_201_CREATED)
async def create_concepto(
    concepto_in: ConceptoCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Crea un nuevo concepto.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden crear conceptos"
        )
    
    # Verificar si ya existe un concepto con el mismo nombre
    existing = crud_concepto.get_concepto_by_nombre(db, nombre=concepto_in.nombre)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un concepto con el nombre '{concepto_in.nombre}'"
        )
    
    concepto = crud_concepto.create_concepto(db, concepto_in=concepto_in)
    return concepto

# ----------------- Endpoint para ACTUALIZAR un concepto -----------------
@router.put("/{concepto_id}", response_model=Concepto)
async def update_concepto(
    concepto_id: int,
    concepto_in: ConceptoUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Actualiza un concepto existente.
    Acceso: Solo administradores y docentes.
    """
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores y docentes pueden actualizar conceptos"
        )
    
    db_concepto = crud_concepto.get_concepto_by_id(db, concepto_id=concepto_id)
    if not db_concepto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concepto no encontrado"
        )
    
    # Si se está cambiando el nombre, verificar que no exista otro con ese nombre
    if concepto_in.nombre and concepto_in.nombre != db_concepto.nombre:
        existing = crud_concepto.get_concepto_by_nombre(db, nombre=concepto_in.nombre)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un concepto con el nombre '{concepto_in.nombre}'"
            )
    
    concepto = crud_concepto.update_concepto(db, db_concepto=db_concepto, concepto_in=concepto_in)
    return concepto

# ----------------- Endpoint para ELIMINAR un concepto -----------------
@router.delete("/{concepto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_concepto(
    concepto_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Elimina un concepto.
    Acceso: Solo administradores.
    """
    if current_user.rol != UserRole.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar conceptos"
        )
    
    db_concepto = crud_concepto.get_concepto_by_id(db, concepto_id=concepto_id)
    if not db_concepto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concepto no encontrado"
        )
    
    crud_concepto.delete_concepto(db, concepto_id=concepto_id)
    return None

