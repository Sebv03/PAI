# backend/app/api/endpoints/recomendaciones.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.crud import crud_recomendacion_estudiante, crud_recurso, crud_task
from app.schemas.recomendacion_estudiante import (
    RecomendacionEstudiante,
    RecomendacionEstudianteCreate,
    RecomendacionEstudianteWithRecurso
)
from app.models.user import User as UserModel
from app.models.user import UserRole

router = APIRouter()

# ----------------- Endpoint para OBTENER recomendaciones del estudiante actual -----------------
@router.get("/me", response_model=List[RecomendacionEstudianteWithRecurso])
async def read_my_recomendaciones(
    solo_no_vistas: bool = False,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene todas las recomendaciones del estudiante autenticado.
    Acceso: Solo estudiantes.
    """
    if current_user.rol != UserRole.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo estudiantes pueden ver sus recomendaciones"
        )
    
    recomendaciones = crud_recomendacion_estudiante.get_recomendaciones_by_estudiante(
        db, estudiante_id=current_user.id, solo_no_vistas=solo_no_vistas
    )
    
    # Enriquecer con información del recurso y tarea
    result = []
    for rec in recomendaciones:
        recurso = crud_recurso.get_recurso_by_id(db, recurso_id=rec.recurso_id)
        tarea = crud_task.get_task_by_id(db, task_id=rec.tarea_id)
        
        rec_dict = {
            "id": rec.id,
            "estudiante_id": rec.estudiante_id,
            "tarea_id": rec.tarea_id,
            "recurso_id": rec.recurso_id,
            "fecha_recomendacion": rec.fecha_recomendacion,
            "vista": rec.vista,
            "fecha_vista": rec.fecha_vista,
            "recurso": {
                "id": recurso.id,
                "titulo": recurso.titulo,
                "tipo": recurso.tipo,
                "url": recurso.url,
                "ruta_archivo": recurso.ruta_archivo,
                "descripcion": recurso.descripcion,
                "duracion_minutos": recurso.duracion_minutos,
                "nivel_dificultad": recurso.nivel_dificultad
            } if recurso else None,
            "tarea": {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion
            } if tarea else None
        }
        result.append(RecomendacionEstudianteWithRecurso(**rec_dict))
    
    return result

# ----------------- Endpoint para MARCAR recomendación como vista -----------------
@router.patch("/{recomendacion_id}/view", response_model=RecomendacionEstudiante)
async def mark_recomendacion_as_viewed(
    recomendacion_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Marca una recomendación como vista.
    Acceso: Solo el estudiante dueño de la recomendación.
    """
    recomendacion = crud_recomendacion_estudiante.get_recomendacion_by_id(db, recomendacion_id=recomendacion_id)
    if not recomendacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada"
        )
    
    # Verificar que el estudiante es el dueño
    if recomendacion.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta recomendación"
        )
    
    recomendacion = crud_recomendacion_estudiante.mark_recomendacion_as_viewed(db, recomendacion_id=recomendacion_id)
    return recomendacion

# ----------------- Endpoint para ELIMINAR una recomendación -----------------
@router.delete("/{recomendacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recomendacion(
    recomendacion_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Elimina una recomendación.
    Acceso: Solo el estudiante dueño de la recomendación.
    """
    recomendacion = crud_recomendacion_estudiante.get_recomendacion_by_id(db, recomendacion_id=recomendacion_id)
    if not recomendacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada"
        )
    
    # Verificar que el estudiante es el dueño
    if recomendacion.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta recomendación"
        )
    
    crud_recomendacion_estudiante.delete_recomendacion(db, recomendacion_id=recomendacion_id)
    return None

# ----------------- Endpoint para OBTENER recomendaciones de un estudiante (Admin/Docente) -----------------
@router.get("/student/{estudiante_id}", response_model=List[RecomendacionEstudianteWithRecurso])
async def read_recomendaciones_by_student(
    estudiante_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene todas las recomendaciones de un estudiante específico.
    Acceso: Administradores, docentes, o el propio estudiante.
    """
    # Verificar permisos
    if current_user.rol == UserRole.ESTUDIANTE and current_user.id != estudiante_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes ver tus propias recomendaciones"
        )
    
    if current_user.rol not in [UserRole.ADMINISTRADOR, UserRole.DOCENTE, UserRole.ESTUDIANTE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver recomendaciones"
        )
    
    recomendaciones = crud_recomendacion_estudiante.get_recomendaciones_by_estudiante(
        db, estudiante_id=estudiante_id, solo_no_vistas=False
    )
    
    # Enriquecer con información del recurso y tarea
    result = []
    for rec in recomendaciones:
        recurso = crud_recurso.get_recurso_by_id(db, recurso_id=rec.recurso_id)
        tarea = crud_task.get_task_by_id(db, task_id=rec.tarea_id)
        
        rec_dict = {
            "id": rec.id,
            "estudiante_id": rec.estudiante_id,
            "tarea_id": rec.tarea_id,
            "recurso_id": rec.recurso_id,
            "fecha_recomendacion": rec.fecha_recomendacion,
            "vista": rec.vista,
            "fecha_vista": rec.fecha_vista,
            "recurso": {
                "id": recurso.id,
                "titulo": recurso.titulo,
                "tipo": recurso.tipo,
                "url": recurso.url,
                "ruta_archivo": recurso.ruta_archivo,
                "descripcion": recurso.descripcion,
                "duracion_minutos": recurso.duracion_minutos,
                "nivel_dificultad": recurso.nivel_dificultad
            } if recurso else None,
            "tarea": {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion
            } if tarea else None
        }
        result.append(RecomendacionEstudianteWithRecurso(**rec_dict))
    
    return result

