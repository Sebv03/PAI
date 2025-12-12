# backend/app/models/exam_question.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"  # Opción múltiple
    ESSAY = "essay"  # Desarrollo

class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Contenido de la pregunta
    texto = Column(Text, nullable=False)  # Texto de la pregunta
    tipo = Column(Enum(QuestionType), nullable=False)  # Tipo: opción múltiple o desarrollo
    puntos = Column(Integer, default=1, nullable=False)  # Puntos que vale la pregunta
    orden = Column(Integer, default=0, nullable=False)  # Orden de la pregunta en el examen
    
    # Relaciones
    exam = relationship("Exam", back_populates="questions")
    opciones = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan", order_by="QuestionOption.orden")

    def __repr__(self):
        return f"<ExamQuestion(id={self.id}, exam_id={self.exam_id}, tipo={self.tipo})>"

class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("exam_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Contenido de la opción
    texto = Column(Text, nullable=False)  # Texto de la opción
    es_correcta = Column(Boolean, default=False, nullable=False)  # Si es la respuesta correcta
    orden = Column(Integer, default=0, nullable=False)  # Orden de la opción
    
    # Relaciones
    question = relationship("ExamQuestion", back_populates="opciones")

    def __repr__(self):
        return f"<QuestionOption(id={self.id}, question_id={self.question_id}, es_correcta={self.es_correcta})>"

