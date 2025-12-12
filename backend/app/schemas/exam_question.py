# backend/app/schemas/exam_question.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.models.exam_question import QuestionType

# --- Question Option Schemas ---

class QuestionOptionBase(BaseModel):
    texto: str
    es_correcta: bool = False
    orden: int = 0

class QuestionOptionCreate(QuestionOptionBase):
    pass

class QuestionOption(QuestionOptionBase):
    id: int
    question_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            question_id=obj.question_id,
            texto=obj.texto,
            es_correcta=obj.es_correcta,
            orden=obj.orden
        )

# --- Question Schemas ---

class ExamQuestionBase(BaseModel):
    texto: str
    tipo: QuestionType
    puntos: int = 1
    orden: int = 0

class ExamQuestionCreate(ExamQuestionBase):
    opciones: Optional[List[QuestionOptionCreate]] = None  # Solo para preguntas de opción múltiple

class ExamQuestion(ExamQuestionBase):
    id: int
    exam_id: int
    opciones: List[QuestionOption] = []
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm(cls, obj):
        opciones_list = []
        if hasattr(obj, 'opciones') and obj.opciones:
            opciones_list = [QuestionOption.from_orm(o) for o in obj.opciones]
        
        return cls(
            id=obj.id,
            exam_id=obj.exam_id,
            texto=obj.texto,
            tipo=obj.tipo,
            puntos=obj.puntos,
            orden=obj.orden,
            opciones=opciones_list
        )

