# backend/app/models/recurso_concepto.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base

class RecursoConcepto(Base):
    """
    Tabla intermedia para la relación many-to-many entre Recursos y Conceptos.
    Permite que un recurso esté asociado a múltiples conceptos y viceversa.
    """
    __tablename__ = "recurso_conceptos"

    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column("recurso_id", Integer, ForeignKey("recursos.id", ondelete="CASCADE"), nullable=False, index=True)
    concepto_id = Column("concepto_id", Integer, ForeignKey("conceptos.id", ondelete="CASCADE"), nullable=False, index=True)
    relevancia = Column("relevancia", Numeric(3, 2), default=1.0, nullable=False)  # Qué tan bien cubre este recurso el concepto (0.0 a 1.0)

    # --- Relaciones de SQLAlchemy ---
    
    # Relación con Recurso
    recurso = relationship("Recurso", back_populates="conceptos")
    
    # Relación con Concepto
    concepto = relationship("Concepto", back_populates="recursos")

    # Constraint único para evitar duplicados
    __table_args__ = (
        UniqueConstraint('recurso_id', 'concepto_id', name='uq_recurso_concepto'),
    )

    def __repr__(self):
        return f"<RecursoConcepto(recurso_id={self.recurso_id}, concepto_id={self.concepto_id}, relevancia={self.relevancia})>"




