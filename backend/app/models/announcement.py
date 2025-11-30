# backend/app/models/announcement.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column("titulo", String(200), nullable=False)
    contenido = Column("contenido", Text, nullable=False)
    
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    fecha_actualizacion = Column("fecha_actualizacion", DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"), nullable=True)
    
    # Claves foráneas
    curso_id = Column("curso_id", Integer, ForeignKey("courses.id"), nullable=False)
    autor_id = Column("autor_id", Integer, ForeignKey("users.id"), nullable=False)

    # --- Relaciones ---
    course = relationship("Course", back_populates="announcements")
    author = relationship("User", back_populates="announcements")
    comments = relationship("Comment", back_populates="announcement", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Announcement(id={self.id}, titulo='{self.titulo}', curso_id={self.curso_id})>"

