# backend/app/schemas/task.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema Base con campos comunes para Pydantic (sin ID, fecha_creacion, etc.)
class TaskBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: datetime

# Esquema para crear una tarea (incluye course_id, que se envía al crear)
class TaskCreate(TaskBase):
    course_id: int # ¡Este campo es fundamental para la creación!

# Esquema para actualizar una tarea (todos los campos son opcionales)
class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_limite: Optional[datetime] = None
    # course_id no se suele cambiar una vez creada la tarea, por eso no lo incluimos aquí.

# Esquema para representar una tarea completa (lo que la API devuelve)
class Task(TaskBase):
    id: int
    curso_id: int # Confirmamos que se devuelve el ID del curso
    fecha_creacion: datetime

    # Configuración para que Pydantic pueda leer modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)