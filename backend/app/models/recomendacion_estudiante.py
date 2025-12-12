# backend/app/models/recomendacion_estudiante.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class RecomendacionEstudiante(Base):
    """
    Modelo para almacenar las recomendaciones de recursos que el sistema genera
    para estudiantes que obtienen notas bajas en tareas específicas.
    """
    __tablename__ = "recomendaciones_estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column("estudiante_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tarea_id = Column("tarea_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    recurso_id = Column("recurso_id", Integer, ForeignKey("recursos.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha_recomendacion = Column("fecha_recomendacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    vista = Column("vista", Boolean, default=False, nullable=False)  # Si el estudiante ya vio la recomendación
    fecha_vista = Column("fecha_vista", DateTime(timezone=True), nullable=True)  # Cuándo la vio

    # --- Relaciones de SQLAlchemy ---
    
    # Relación con Estudiante
    estudiante = relationship("User", back_populates="recomendaciones")
    
    # Relación con Tarea
    tarea = relationship("Task", back_populates="recomendaciones")
    
    # Relación con Recurso
    recurso = relationship("Recurso", back_populates="recomendaciones")

    # Constraint único para evitar duplicados
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'tarea_id', 'recurso_id', name='uq_recomendacion_estudiante'),
    )

    def __repr__(self):
        return f"<RecomendacionEstudiante(id={self.id}, estudiante_id={self.estudiante_id}, tarea_id={self.tarea_id}, recurso_id={self.recurso_id}, vista={self.vista})>"




