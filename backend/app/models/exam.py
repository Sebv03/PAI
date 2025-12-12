from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)  # Title
    descripcion = Column(Text, nullable=True)  # Description
    fecha_programada = Column(DateTime, nullable=True)  # Scheduled Date
    curso_id = Column(Integer, ForeignKey("courses.id"))
    
    # PDF del examen (opcional)
    ruta_pdf = Column(String(500), nullable=True)  # Ruta al archivo PDF del examen
    
    # Audit
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relaciones
    curso = relationship("Course", back_populates="exams")
    submissions = relationship("ExamSubmission", back_populates="exam", cascade="all, delete-orphan")
    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan", order_by="ExamQuestion.orden")

class ExamSubmission(Base):
    __tablename__ = "exam_submissions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    estudiante_id = Column(Integer, ForeignKey("users.id"))
    
    contenido = Column(Text, nullable=True) # Text answers
    fecha_entrega = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    calificacion = Column(Float, nullable=True) # 1.0 to 7.0
    retroalimentacion = Column(Text, nullable=True) # Feedback
    
    # Relaciones
    exam = relationship("Exam", back_populates="submissions")
    estudiante = relationship("User", back_populates="exam_submissions")
