# backend/app/schemas/submission.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Campos que se comparten (base)
class SubmissionBase(BaseModel):
    content: Optional[str] = None  # Mantenemos en inglés para compatibilidad con el frontend
    file_path: Optional[str] = None  # Mantenemos en inglés para compatibilidad con el frontend

# Esquema para crear una entrega (lo que envía el estudiante)
# El student_id vendrá del token
# El task_id vendrá de la URL
class SubmissionCreate(SubmissionBase):
    pass # Solo necesita el contenido o el archivo

# Esquema para actualizar (ej. un docente añade nota)
class SubmissionUpdate(BaseModel):
    content: Optional[str] = None
    grade: Optional[float] = None  # Nota de 0 a 100
    feedback: Optional[str] = None  # Comentarios del docente

# Esquema para leer una entrega (lo que la API devuelve)
class Submission(SubmissionBase):
    id: int
    student_id: int
    task_id: int
    submitted_at: datetime
    file_path: Optional[str] = None  # Ruta del archivo PDF si existe
    grade: Optional[float] = None  # Calificación (0 a 100)
    feedback: Optional[str] = None  # Feedback del docente
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm(cls, obj):
        """Mapea los campos del modelo (español) al schema (inglés para compatibilidad)"""
        return cls(
            id=obj.id,
            student_id=obj.estudiante_id,
            task_id=obj.tarea_id,
            submitted_at=obj.fecha_entrega,
            content=obj.contenido,
            file_path=obj.ruta_archivo,
            grade=obj.calificacion,
            feedback=obj.retroalimentacion
        )

# Esquema extendido que incluye información del estudiante (útil para docentes)
# Este schema se usa cuando se devuelven entregas con información adicional del estudiante
class SubmissionWithStudent(Submission):
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)