# backend/app/schemas/recurso.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema base para Recurso
class RecursoBase(BaseModel):
    titulo: str
    tipo: str  # video_youtube, pdf, ejercicio_interactivo, articulo
    url: Optional[str] = None
    ruta_archivo: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    nivel_dificultad: Optional[str] = None  # básico, intermedio, avanzado
    autor: Optional[str] = None

# Esquema para crear un recurso
class RecursoCreate(RecursoBase):
    activo: bool = True

# Esquema para actualizar un recurso
class RecursoUpdate(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    url: Optional[str] = None
    ruta_archivo: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    nivel_dificultad: Optional[str] = None
    autor: Optional[str] = None
    activo: Optional[bool] = None

# Esquema para representar un recurso completo
class Recurso(RecursoBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Esquema extendido que incluye conceptos asociados
class RecursoWithConcepts(Recurso):
    conceptos: list = []  # Lista de conceptos asociados
    
    model_config = ConfigDict(from_attributes=True)




