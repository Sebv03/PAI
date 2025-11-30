# backend/app/schemas/course.py
from typing import Optional, List
from pydantic import BaseModel

from app.schemas.user import User as UserSchema # Importa el esquema de User para anidarlo

# Esquema base para la creación de un curso
class CourseCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None # La descripción puede ser opcional al crear

# Esquema para la actualización de un curso
class CourseUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None

# Esquema principal para la respuesta del curso (lo que se devuelve por la API)
class Course(BaseModel): # NOTA: Se llama igual que el modelo, pero es el esquema Pydantic
    id: int
    titulo: str
    descripcion: Optional[str] = None
    propietario_id: int # El ID del propietario
    propietario_nombre: Optional[str] = None  # Nombre del profesor
    propietario_correo: Optional[str] = None  # Email del profesor
    fecha_creacion: Optional[str] = None  # Fecha de creación

    # Opcional: Para incluir el objeto completo del propietario si se desea en algunas respuestas
    # owner: UserSchema # Descomentar si quieres incrustar el objeto User completo

    class Config:
        orm_mode = True # Permite que Pydantic lea directamente de un objeto SQLAlchemy
        from_attributes = True # Pydantic v2: Usa from_attributes en lugar de orm_mode