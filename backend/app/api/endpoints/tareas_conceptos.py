# backend/app/api/endpoints/tareas_conceptos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.crud import crud_tarea_concepto, crud_task, crud_course
from app.schemas.tarea_concepto import TareaConceptosCreate, TareaConcepto
from app.models.user import User as UserModel
from app.models.user import UserRole

router = APIRouter()

# ----------------- Endpoint para ASOCIAR conceptos a una tarea -----------------
@router.post("/tasks/{task_id}/conceptos", response_model=List[TareaConcepto])
async def associate_conceptos_to_task(
    task_id: int,
    conceptos_in: TareaConceptosCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Asocia múltiples conceptos a una tarea.
    Acceso: Solo el docente propietario del curso o administradores.
    """
    # Verificar que la tarea existe
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    # Verificar permisos: solo docente propietario o admin
    course = crud_course.get_course_by_id(db, course_id=task.curso_id)
    if course.propietario_id != current_user.id and current_user.rol != UserRole.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el docente del curso puede asociar conceptos a tareas"
        )
    
    # Validar que se proporcionen conceptos
    if not conceptos_in.concepto_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes proporcionar al menos un concepto"
        )
    
    # Asociar conceptos
    relaciones = crud_tarea_concepto.associate_conceptos_to_tarea(
        db,
        tarea_id=task_id,
        concepto_ids=conceptos_in.concepto_ids,
        pesos=conceptos_in.pesos
    )
    
    return relaciones

# ----------------- Endpoint para OBTENER conceptos de una tarea -----------------
@router.get("/tasks/{task_id}/conceptos", response_model=List[TareaConcepto])
async def get_conceptos_by_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene todos los conceptos asociados a una tarea.
    Acceso: Cualquier usuario autenticado.
    """
    # Verificar que la tarea existe
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    relaciones = crud_tarea_concepto.get_conceptos_by_tarea(db, tarea_id=task_id)
    return relaciones

# ----------------- Endpoint para ELIMINAR conceptos de una tarea -----------------
@router.delete("/tasks/{task_id}/conceptos", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conceptos_from_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Elimina todas las asociaciones de conceptos de una tarea.
    Acceso: Solo el docente propietario del curso o administradores.
    """
    # Verificar que la tarea existe
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    # Verificar permisos
    course = crud_course.get_course_by_id(db, course_id=task.curso_id)
    if course.propietario_id != current_user.id and current_user.rol != UserRole.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el docente del curso puede eliminar conceptos de tareas"
        )
    
    crud_tarea_concepto.delete_all_tarea_conceptos(db, tarea_id=task_id)
    return None

