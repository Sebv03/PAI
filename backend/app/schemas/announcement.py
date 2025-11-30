# backend/app/schemas/announcement.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Esquema base para comunicados
class AnnouncementBase(BaseModel):
    titulo: str
    contenido: str

# Esquema para crear un comunicado
class AnnouncementCreate(AnnouncementBase):
    pass

# Esquema para actualizar un comunicado
class AnnouncementUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None

# Esquema para leer un comunicado (con información del autor)
class Announcement(AnnouncementBase):
    id: int
    curso_id: int
    autor_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    autor_nombre: Optional[str] = None
    autor_correo: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Esquema para comentarios
class CommentBase(BaseModel):
    contenido: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    anuncio_id: int
    autor_id: int
    fecha_creacion: datetime
    autor_nombre: Optional[str] = None
    autor_correo: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Esquema extendido que incluye comentarios
class AnnouncementWithComments(Announcement):
    comments: List[Comment] = []

