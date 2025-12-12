# backend/app/schemas/interaccion_recurso.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema base para InteraccionRecurso
class InteraccionRecursoBase(BaseModel):
    estudiante_id: int
    recurso_id: int
    tipo_interaccion: Optional[str] = None  # viewed, completed, rated
    calificacion: Optional[int] = None  # 1-5 estrellas
    tiempo_visto_segundos: Optional[int] = None
    mejora_nota: Optional[bool] = False

# Esquema para crear una interacción
class InteraccionRecursoCreate(InteraccionRecursoBase):
    pass

# Esquema para actualizar una interacción
class InteraccionRecursoUpdate(BaseModel):
    tipo_interaccion: Optional[str] = None
    calificacion: Optional[int] = None
    tiempo_visto_segundos: Optional[int] = None
    mejora_nota: Optional[bool] = None

# Esquema para representar una interacción completa
class InteraccionRecurso(InteraccionRecursoBase):
    id: int
    fecha_interaccion: datetime
    
    model_config = ConfigDict(from_attributes=True)




