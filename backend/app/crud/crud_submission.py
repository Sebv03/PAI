# backend/app/crud/crud_submission.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionUpdate

# ----------------- Crear una nueva entrega -----------------
def create_submission(db: Session, submission_in: SubmissionCreate, task_id: int, student_id: int, file_path: Optional[str] = None) -> Submission:
    """
    Crea una nueva entrega para una tarea específica por un estudiante específico.
    """
    from datetime import datetime, timezone
    
    # Establecer la fecha explícitamente
    fecha_entrega = datetime.now(timezone.utc)
    
    db_submission = Submission(
        contenido=submission_in.content,  # Ahora puede ser None (nullable)
        ruta_archivo=file_path or submission_in.file_path,
        tarea_id=task_id,
        estudiante_id=student_id,
        fecha_entrega=fecha_entrega  # Establecer explícitamente la fecha
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission, attribute_names=['fecha_entrega'])  # Refresh específico del campo
    
    # Asegurarse de que la fecha esté disponible (si aún es None, establecerla)
    if db_submission.fecha_entrega is None:
        db_submission.fecha_entrega = fecha_entrega
        # Actualizar en la base de datos si es necesario
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
    
    return db_submission

# ----------------- Obtener una entrega por ID -----------------
def get_submission_by_id(db: Session, submission_id: int) -> Optional[Submission]:
    """
    Obtiene una entrega específica por su ID.
    """
    return db.query(Submission).filter(Submission.id == submission_id).first()

# ----------------- Obtener entregas por Task ID -----------------
def get_submissions_by_task(db: Session, task_id: int, skip: int = 0, limit: int = 100) -> List[Submission]:
    """
    Obtiene todas las entregas de una tarea específica.
    Incluye la relación con el estudiante para acceder a su información.
    """
    return db.query(Submission).filter(Submission.tarea_id == task_id).offset(skip).limit(limit).all()

# ----------------- Obtener la entrega de un estudiante para una tarea -----------------
def get_submission_by_task_and_student(db: Session, task_id: int, student_id: int) -> Optional[Submission]:
    """
    Verifica si un estudiante ya entregó una tarea específica.
    """
    from sqlalchemy import and_
    return db.query(Submission).filter(
        and_(Submission.tarea_id == task_id, Submission.estudiante_id == student_id)
    ).first()

# ----------------- Actualizar una entrega (para calificar) -----------------
def update_submission(db: Session, db_submission: Submission, submission_in: SubmissionUpdate) -> Submission:
    """
    Actualiza una entrega existente (ej. para añadir nota o feedback).
    """
    update_data = submission_in.model_dump(exclude_unset=True) 

    # Mapear campos del schema (inglés) al modelo (español)
    field_mapping = {
        'content': 'contenido',
        'grade': 'calificacion',
        'feedback': 'retroalimentacion'
    }

    for field, value in update_data.items():
        model_field = field_mapping.get(field, field)
        setattr(db_submission, model_field, value)

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

# ----------------- Eliminar una entrega -----------------
def delete_submission(db: Session, submission_id: int) -> Optional[Submission]:
    """
    Elimina una entrega específica por su ID.
    """
    db_submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if db_submission:
        db.delete(db_submission)
        db.commit()
    return db_submission