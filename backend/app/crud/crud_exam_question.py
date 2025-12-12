# backend/app/crud/crud_exam_question.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.exam_question import ExamQuestion, QuestionOption
from app.schemas.exam_question import ExamQuestionCreate, QuestionOptionCreate

def get_question_by_id(db: Session, question_id: int) -> Optional[ExamQuestion]:
    return db.query(ExamQuestion).filter(ExamQuestion.id == question_id).first()

def get_questions_by_exam(db: Session, exam_id: int) -> List[ExamQuestion]:
    return db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam_id).order_by(ExamQuestion.orden).all()

def create_question(db: Session, question_in: ExamQuestionCreate, exam_id: int) -> ExamQuestion:
    db_question = ExamQuestion(
        exam_id=exam_id,
        texto=question_in.texto,
        tipo=question_in.tipo,
        puntos=question_in.puntos,
        orden=question_in.orden
    )
    db.add(db_question)
    db.flush()  # Para obtener el ID sin hacer commit
    
    # Si es pregunta de opción múltiple, crear las opciones
    if question_in.tipo.value == "multiple_choice" and question_in.opciones:
        for opcion_in in question_in.opciones:
            db_opcion = QuestionOption(
                question_id=db_question.id,
                texto=opcion_in.texto,
                es_correcta=opcion_in.es_correcta,
                orden=opcion_in.orden
            )
            db.add(db_opcion)
    
    db.commit()
    db.refresh(db_question)
    return db_question

def create_questions_bulk(db: Session, questions_in: List[ExamQuestionCreate], exam_id: int) -> List[ExamQuestion]:
    """Crea múltiples preguntas para un examen"""
    created_questions = []
    for idx, question_in in enumerate(questions_in):
        # Si no tiene orden, usar el índice
        if question_in.orden == 0:
            question_in.orden = idx + 1
        question = create_question(db, question_in, exam_id)
        created_questions.append(question)
    return created_questions

def delete_question(db: Session, question_id: int) -> bool:
    question = get_question_by_id(db, question_id)
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True

