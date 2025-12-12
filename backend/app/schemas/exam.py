from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .exam_question import ExamQuestionCreate, ExamQuestion

# --- Exam Schemas ---

class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class ExamCreate(ExamBase):
    course_id: int
    questions: Optional[List[ExamQuestionCreate]] = None  # Preguntas del examen

class ExamUpdate(ExamBase):
    title: Optional[str] = None
    course_id: Optional[int] = None

class Exam(ExamBase):
    id: int
    course_id: int
    created_at: datetime
    pdf_path: Optional[str] = None  # Ruta al PDF del examen
    questions: List[ExamQuestion] = []  # Preguntas del examen
    
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj, questions=None):
        # Si no se pasan preguntas, intentar obtenerlas del objeto si tiene relación cargada
        questions_list = []
        if questions:
            questions_list = [ExamQuestion.from_orm(q) for q in questions]
        elif hasattr(obj, 'questions') and obj.questions:
            questions_list = [ExamQuestion.from_orm(q) for q in obj.questions]
        
        return cls(
            id=obj.id,
            title=obj.titulo,
            description=obj.descripcion,
            scheduled_at=obj.fecha_programada,
            course_id=obj.curso_id,
            created_at=obj.creado_en,
            pdf_path=obj.ruta_pdf,
            questions=questions_list
        )

# --- Submission Schemas ---

class ExamSubmissionBase(BaseModel):
    content: Optional[str] = None

class ExamSubmissionCreate(ExamSubmissionBase):
    pass

class ExamSubmissionUpdate(BaseModel):
    grade: float # 1.0 to 7.0
    feedback: Optional[str] = None

class ExamSubmission(ExamSubmissionBase):
    id: int
    exam_id: int
    student_id: int
    submitted_at: datetime
    grade: Optional[float] = None
    feedback: Optional[str] = None
    
    # Extra fields for list view
    student_name: Optional[str] = None
    student_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            exam_id=obj.exam_id,
            student_id=obj.estudiante_id,
            submitted_at=obj.fecha_entrega,
            content=obj.contenido,
            grade=obj.calificacion,
            feedback=obj.retroalimentacion
        )
