# backend/app/models/recurso.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class TipoRecurso(str):
    """Enum para tipos de recursos (usado como string en la BD)"""
    VIDEO_YOUTUBE = "video_youtube"
    PDF = "pdf"
    EJERCICIO_INTERACTIVO = "ejercicio_interactivo"
    ARTICULO = "articulo"
    VIDEO_LOCAL = "video_local"

class NivelDificultad(str):
    """Enum para niveles de dificultad (usado como string en la BD)"""
    BASICO = "básico"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"

class Recurso(Base):
    """
    Modelo para representar recursos remediales (videos, PDFs, ejercicios, etc.)
    que ayudan a los estudiantes a mejorar en conceptos específicos.
    """
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column("titulo", String(255), nullable=False, index=True)
    tipo = Column("tipo", String(50), nullable=False)  # video_youtube, pdf, ejercicio_interactivo, articulo
    url = Column("url", String(500), nullable=True)  # Para videos y artículos externos
    ruta_archivo = Column("ruta_archivo", String(500), nullable=True)  # Para PDFs locales
    descripcion = Column("descripcion", Text, nullable=True)
    duracion_minutos = Column("duracion_minutos", Integer, nullable=True)  # Para videos
    nivel_dificultad = Column("nivel_dificultad", String(50), nullable=True)  # básico, intermedio, avanzado
    autor = Column("autor", String(255), nullable=True)
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    activo = Column("activo", Boolean, default=True, nullable=False)

    # --- Relaciones de SQLAlchemy ---
    
    # Relación many-to-many con Conceptos (a través de recurso_conceptos)
    conceptos = relationship("RecursoConcepto", back_populates="recurso", cascade="all, delete-orphan")
    
    # Relación con Recomendaciones (un recurso puede estar en muchas recomendaciones)
    recomendaciones = relationship("RecomendacionEstudiante", back_populates="recurso", cascade="all, delete-orphan")
    
    # Relación con Interacciones (un recurso puede tener muchas interacciones)
    interacciones = relationship("InteraccionRecurso", back_populates="recurso", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Recurso(id={self.id}, titulo='{self.titulo}', tipo='{self.tipo}')>"




