# backend/app/models/interaccion_recurso.py
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class TipoInteraccion(str):
    """Enum para tipos de interacción (usado como string en la BD)"""
    VIEWED = "viewed"  # Visto
    COMPLETED = "completed"  # Completado
    RATED = "rated"  # Calificado

class InteraccionRecurso(Base):
    """
    Modelo para rastrear las interacciones de estudiantes con recursos.
    Útil para el futuro Nivel 3 (Collaborative Filtering) y para analizar
    la efectividad de los recursos.
    """
    __tablename__ = "interacciones_recursos"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column("estudiante_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recurso_id = Column("recurso_id", Integer, ForeignKey("recursos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_interaccion = Column("tipo_interaccion", String(50), nullable=True)  # viewed, completed, rated
    calificacion = Column("calificacion", Integer, nullable=True)  # 1-5 estrellas (opcional)
    tiempo_visto_segundos = Column("tiempo_visto_segundos", Integer, nullable=True)  # Para videos
    fecha_interaccion = Column("fecha_interaccion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    mejora_nota = Column("mejora_nota", Boolean, default=False, nullable=False)  # Si mejoró después de ver el recurso

    # --- Relaciones de SQLAlchemy ---
    
    # Relación con Estudiante
    estudiante = relationship("User", back_populates="interacciones_recursos")
    
    # Relación con Recurso
    recurso = relationship("Recurso", back_populates="interacciones")

    def __repr__(self):
        return f"<InteraccionRecurso(id={self.id}, estudiante_id={self.estudiante_id}, recurso_id={self.recurso_id}, tipo='{self.tipo_interaccion}')>"




