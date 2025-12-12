from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.models.exam import Exam, ExamSubmission
from app.schemas.exam import ExamCreate, ExamUpdate, ExamSubmissionCreate, ExamSubmissionUpdate

# --- EXAM CRUD ---

def get_exam(db: Session, exam_id: int) -> Optional[Exam]:
    return db.query(Exam).filter(Exam.id == exam_id).first()

def get_exams_by_course(db: Session, course_id: int) -> List[Exam]:
    return db.query(Exam).filter(Exam.curso_id == course_id).order_by(Exam.fecha_programada.desc()).all()

def create_exam(db: Session, exam_in: ExamCreate) -> Exam:
    db_exam = Exam(
        titulo=exam_in.title,
        descripcion=exam_in.description,
        fecha_programada=exam_in.scheduled_at,
        curso_id=exam_in.course_id
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

# --- SUBMISSION CRUD ---

def get_submission(db: Session, submission_id: int) -> Optional[ExamSubmission]:
    return db.query(ExamSubmission).filter(ExamSubmission.id == submission_id).first()

def get_submission_by_student(db: Session, exam_id: int, student_id: int) -> Optional[ExamSubmission]:
    return db.query(ExamSubmission).filter(
        ExamSubmission.exam_id == exam_id,
        ExamSubmission.estudiante_id == student_id
    ).first()

def get_submissions_by_exam(db: Session, exam_id: int) -> List[ExamSubmission]:
    return db.query(ExamSubmission).filter(ExamSubmission.exam_id == exam_id).all()

def create_submission(db: Session, submission_in: ExamSubmissionCreate, exam_id: int, student_id: int) -> ExamSubmission:
    db_submission = ExamSubmission(
        exam_id=exam_id,
        estudiante_id=student_id,
        contenido=submission_in.content,
        fecha_entrega=datetime.now(timezone.utc)
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def update_submission_grade(db: Session, db_submission: ExamSubmission, update_in: ExamSubmissionUpdate) -> ExamSubmission:
    db_submission.calificacion = update_in.grade
    db_submission.retroalimentacion = update_in.feedback
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission
