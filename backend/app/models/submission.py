# backend/app/models/submission.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text # Para el valor por defecto NOW()

from app.db.base import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Contenido de la entrega (puede ser un texto o un enlace a un archivo)
    contenido = Column("contenido", Text, nullable=True)
    
    # Ruta del archivo PDF subido (si se entrega un PDF)
    ruta_archivo = Column("ruta_archivo", String(500), nullable=True) 
    
    # Calificación (nota de 1.0 a 7.0)
    calificacion = Column("calificacion", Float, nullable=True)
    
    # Feedback del docente
    retroalimentacion = Column("retroalimentacion", Text, nullable=True)
    
    # Fecha de entrega (manejada por la base de datos)
    fecha_entrega = Column("fecha_entrega", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)

    # Claves foráneas
    estudiante_id = Column("estudiante_id", Integer, ForeignKey("users.id"), nullable=False)
    tarea_id = Column("tarea_id", Integer, ForeignKey("tasks.id"), nullable=False)

    # --- Relaciones de SQLAlchemy ---
    
    # Relación de vuelta al Estudiante (Un usuario tiene muchas entregas)
    student = relationship("User", back_populates="submissions", foreign_keys=[estudiante_id])
    
    # Relación de vuelta a la Tarea (Una tarea tiene muchas entregas)
    task = relationship("Task", back_populates="submissions", foreign_keys=[tarea_id])

    def __repr__(self):
        return f"<Submission(id={self.id}, estudiante_id={self.estudiante_id}, tarea_id={self.tarea_id})>"