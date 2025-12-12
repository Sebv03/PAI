# backend/app/schemas/recomendacion_estudiante.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema base para RecomendacionEstudiante
class RecomendacionEstudianteBase(BaseModel):
    estudiante_id: int
    tarea_id: int
    recurso_id: int

# Esquema para crear una recomendación
class RecomendacionEstudianteCreate(RecomendacionEstudianteBase):
    pass

# Esquema para actualizar una recomendación
class RecomendacionEstudianteUpdate(BaseModel):
    vista: Optional[bool] = None
    fecha_vista: Optional[datetime] = None

# Esquema para representar una recomendación completa
class RecomendacionEstudiante(RecomendacionEstudianteBase):
    id: int
    fecha_recomendacion: datetime
    vista: bool
    fecha_vista: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Esquema extendido que incluye información del recurso
class RecomendacionEstudianteWithRecurso(RecomendacionEstudiante):
    recurso: Optional[dict] = None  # Información del recurso
    tarea: Optional[dict] = None  # Información de la tarea
    
    model_config = ConfigDict(from_attributes=True)




