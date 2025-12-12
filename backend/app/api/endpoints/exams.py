from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from datetime import datetime
from pathlib import Path
import shutil
import json

from app.api import deps
from app.crud import crud_exam, crud_course, crud_user, crud_exam_question
from app.schemas.exam import Exam, ExamCreate, ExamSubmission, ExamSubmissionCreate, ExamSubmissionUpdate
from app.schemas.exam_question import ExamQuestionCreate
from app.models.user import User as UserModel, UserRole
from app.core.config import settings

router = APIRouter()

# --- Exams ---

@router.post("/", response_model=Exam)
async def create_exam(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    scheduled_at: Optional[str] = Form(None),
    course_id: int = Form(...),
    pdf_file: Optional[UploadFile] = File(None),
    questions_json: Optional[str] = Form(None),  # JSON string con las preguntas
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """Create a new exam with optional PDF and questions (Teacher/Admin only)"""
    course = crud_course.get_course_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    if current_user.rol != UserRole.ADMINISTRADOR and current_user.id != course.propietario_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Parsear fecha si viene
    fecha_programada = None
    if scheduled_at:
        try:
            fecha_programada = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        except:
            pass
    
    # Manejar archivo PDF si se envió
    pdf_path = None
    if pdf_file:
        # Validar que sea un PDF
        if not pdf_file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten archivos PDF."
            )
        
        # Crear directorio de uploads si no existe
        upload_dir = Path(settings.UPLOAD_DIR).parent / "exams"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre único para el archivo
        file_name = f"exam_{course_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = str(upload_dir / file_name)
        
        # Guardar el archivo
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
    
    # Crear el examen
    exam_in = ExamCreate(
        title=title,
        description=description,
        scheduled_at=fecha_programada,
        course_id=course_id,
        questions=None  # Las preguntas se crearán después
    )
    
    exam = crud_exam.create_exam(db, exam_in)
    
    # Actualizar ruta del PDF si existe
    if pdf_path:
        exam.ruta_pdf = pdf_path
        db.commit()
        db.refresh(exam)
    
    # Crear preguntas si se enviaron
    questions_created = []
    if questions_json:
        try:
            questions_data = json.loads(questions_json)
            questions_list = [ExamQuestionCreate(**q) for q in questions_data]
            questions_created = crud_exam_question.create_questions_bulk(db, questions_list, exam.id)
        except Exception as e:
            print(f"Error al crear preguntas: {e}")
            # No fallar si hay error en las preguntas, el examen ya está creado
    
    # Cargar preguntas para la respuesta
    questions = crud_exam_question.get_questions_by_exam(db, exam.id)
    return Exam.from_orm(exam, questions=questions)

@router.get("/course/{course_id}", response_model=List[Exam])
async def read_exams_by_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """List exams for a course"""
    # Check access (anyone enrolled or owner/admin)
    # Ideally check enrollment, for now assumes user has basic access to platform
    exams = crud_exam.get_exams_by_course(db, course_id)
    result = []
    for exam in exams:
        questions = crud_exam_question.get_questions_by_exam(db, exam.id)
        result.append(Exam.from_orm(exam, questions=questions))
    return result

@router.get("/{exam_id}", response_model=Exam)
async def read_exam(
    exam_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    exam = crud_exam.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    questions = crud_exam_question.get_questions_by_exam(db, exam_id)
    return Exam.from_orm(exam, questions=questions)

# --- Submissions ---

@router.post("/{exam_id}/submit", response_model=ExamSubmission)
async def submit_exam(
    exam_id: int,
    submission_in: ExamSubmissionCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """Submit an exam (Student only)"""
    if current_user.rol != UserRole.ESTUDIANTE:
        raise HTTPException(status_code=403, detail="Only students can submit exams")
    
    exam = crud_exam.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
        
    # Check if already submitted
    existing = crud_exam.get_submission_by_student(db, exam_id, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Already submitted")
        
    submission = crud_exam.create_submission(db, submission_in, exam_id, current_user.id)
    return ExamSubmission.from_orm(submission)

@router.get("/{exam_id}/my-submission", response_model=ExamSubmission)
async def read_my_submission(
    exam_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    submission = crud_exam.get_submission_by_student(db, exam_id, current_user.id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return ExamSubmission.from_orm(submission)

@router.get("/{exam_id}/submissions", response_model=List[ExamSubmission])
async def read_all_submissions(
    exam_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """Read all submissions for an exam (Teacher/Admin only)"""
    exam = crud_exam.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    course = crud_course.get_course_by_id(db, exam.curso_id)
    if current_user.rol != UserRole.ADMINISTRADOR and current_user.id != course.propietario_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    submissions = crud_exam.get_submissions_by_exam(db, exam_id)
    
    # Enrich with student info
    result = []
    for sub in submissions:
        student = crud_user.get_user_by_id(db, sub.estudiante_id)
        s_obj = ExamSubmission.from_orm(sub)
        if student:
            s_obj.student_name = student.nombre_completo or f"User {student.id}"
            s_obj.student_email = student.correo
        result.append(s_obj)
        
    return result

@router.put("/submissions/{submission_id}", response_model=ExamSubmission)
async def grade_submission(
    submission_id: int,
    update_in: ExamSubmissionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """Grade a submission (Teacher/Admin) - Scale 1.0 to 7.0"""
    submission = crud_exam.get_submission(db, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    exam = crud_exam.get_exam(db, submission.exam_id)
    course = crud_course.get_course_by_id(db, exam.curso_id)
    
    if current_user.rol != UserRole.ADMINISTRADOR and current_user.id != course.propietario_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate Grade 1.0 - 7.0
    if update_in.grade < 1.0 or update_in.grade > 7.0:
        raise HTTPException(status_code=400, detail="Grade must be between 1.0 and 7.0")
        
    updated = crud_exam.update_submission_grade(db, submission, update_in)
    return ExamSubmission.from_orm(updated)
