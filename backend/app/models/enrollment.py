# backend/app/models/enrollment.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.sql import text


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    fecha_inscripcion = Column("fecha_inscripcion", DateTime, server_default=text("NOW()"), nullable=False)

    # Foreign Keys
    estudiante_id = Column("estudiante_id", Integer, ForeignKey("users.id"), nullable=False)
    curso_id = Column("curso_id", Integer, ForeignKey("courses.id"), nullable=False)

    # --- RELACIONES ---
    # Una inscripción pertenece a un estudiante (User)
    student = relationship("User", back_populates="enrollments", foreign_keys=[estudiante_id]) # <--- USA CADENA

    # Una inscripción pertenece a un curso (Course)
    course = relationship("Course", back_populates="enrollments", foreign_keys=[curso_id]) # <--- USA CADENA

    def __repr__(self):
        return f"<Enrollment(id={self.id}, estudiante_id={self.estudiante_id}, curso_id={self.curso_id})>"