# backend/app/models/concepto.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class Concepto(Base):
    """
    Modelo para representar conceptos o habilidades pedagógicas.
    Ejemplos: "Álgebra Básica", "Ecuaciones 2do Grado", "Comprensión Lectora Inferencial"
    """
    __tablename__ = "conceptos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column("nombre", String(255), unique=True, nullable=False, index=True)
    descripcion = Column("descripcion", Text, nullable=True)
    categoria = Column("categoria", String(100), nullable=True)  # ej: "Matemáticas", "Lenguaje", "Ciencias"
    nivel = Column("nivel", String(50), nullable=True)  # ej: "Básico", "Intermedio", "Avanzado"
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)

    # --- Relaciones de SQLAlchemy ---
    
    # Relación many-to-many con Tareas (a través de tarea_conceptos)
    tareas = relationship("TareaConcepto", back_populates="concepto", cascade="all, delete-orphan")
    
    # Relación many-to-many con Recursos (a través de recurso_conceptos)
    recursos = relationship("RecursoConcepto", back_populates="concepto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Concepto(id={self.id}, nombre='{self.nombre}', categoria='{self.categoria}')>"




