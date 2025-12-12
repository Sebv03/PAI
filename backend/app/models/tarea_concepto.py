# backend/app/models/tarea_concepto.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base

class TareaConcepto(Base):
    """
    Tabla intermedia para la relación many-to-many entre Tareas y Conceptos.
    Permite que una tarea esté asociada a múltiples conceptos y viceversa.
    """
    __tablename__ = "tarea_conceptos"

    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column("tarea_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    concepto_id = Column("concepto_id", Integer, ForeignKey("conceptos.id", ondelete="CASCADE"), nullable=False, index=True)
    peso = Column("peso", Numeric(3, 2), default=1.0, nullable=False)  # Qué tan relevante es el concepto para esta tarea (0.0 a 1.0)

    # --- Relaciones de SQLAlchemy ---
    
    # Relación con Tarea
    tarea = relationship("Task", back_populates="conceptos")
    
    # Relación con Concepto
    concepto = relationship("Concepto", back_populates="tareas")

    # Constraint único para evitar duplicados
    __table_args__ = (
        UniqueConstraint('tarea_id', 'concepto_id', name='uq_tarea_concepto'),
    )

    def __repr__(self):
        return f"<TareaConcepto(tarea_id={self.tarea_id}, concepto_id={self.concepto_id}, peso={self.peso})>"




