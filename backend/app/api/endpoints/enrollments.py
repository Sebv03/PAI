from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.crud import crud_enrollment, crud_course
from app.schemas.enrollment import Enrollment, EnrollmentCreate # Asegúrate que EnrollmentCreate esté en schemas/enrollment.py
from app.schemas.course import Course as CourseSchema # Usamos el schema de Course para la respuesta
from app.models.user import User as UserModel
from app.models.user import UserRole

router = APIRouter()

# ----------------- Endpoint para OBTENER los cursos inscritos del ESTUDIANTE actual -----------------
@router.get("/me/courses", response_model=List[CourseSchema])
async def read_my_enrolled_courses(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene la lista de cursos en los que el estudiante actual está inscrito.
    """
    from app.crud import crud_user
    from datetime import datetime
    
    if current_user.rol != UserRole.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Solo los estudiantes pueden ver sus cursos inscritos."
        )
        
    courses = crud_enrollment.get_enrolled_courses_by_student(db, student_id=current_user.id)
    
    # Agregar información del profesor a cada curso
    result = []
    for course in courses:
        owner = crud_user.get_user_by_id(db, user_id=course.propietario_id)
        course_dict = {
            "id": course.id,
            "titulo": course.titulo,
            "descripcion": course.descripcion,
            "propietario_id": course.propietario_id,
            "propietario_nombre": None,
            "propietario_correo": None,
            "fecha_creacion": None
        }
        if owner:
            course_dict["propietario_nombre"] = owner.nombre_completo or f"Usuario {owner.id}"
            course_dict["propietario_correo"] = owner.correo
        if hasattr(course, 'fecha_creacion') and course.fecha_creacion:
            course_dict["fecha_creacion"] = course.fecha_creacion.isoformat() if isinstance(course.fecha_creacion, datetime) else str(course.fecha_creacion)
        result.append(CourseSchema(**course_dict))
    
    return result

# Mantener el endpoint anterior por compatibilidad (deprecated)
@router.get("/me", response_model=List[CourseSchema])
async def read_my_enrollments(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    [DEPRECATED] Usa /me/courses en su lugar.
    Obtiene la lista de cursos en los que el estudiante actual está inscrito.
    """
    return await read_my_enrolled_courses(db, current_user)

# ----------------- Endpoint para INSCRIBIR al ESTUDIANTE actual en un curso -----------------
@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def enroll_student_in_course(
    enrollment_in: EnrollmentCreate, # Recibimos el course_id desde el schema
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Inscribe al usuario (estudiante) actual en un curso.
    """
    if current_user.rol != UserRole.ESTUDIANTE:
        raise HTTPException(status_code=403, detail="Solo los estudiantes pueden inscribirse en cursos.")

    course = crud_course.get_course_by_id(db, course_id=enrollment_in.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado.")

    # Verificar que el estudiante no sea el dueño del curso (un docente no se inscribe a su propio curso)
    if course.propietario_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes inscribirte en tu propio curso.")

    existing = crud_enrollment.get_enrollment_by_user_and_course(db, student_id=current_user.id, course_id=enrollment_in.course_id)
    if existing:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso.")
    
    enrollment = crud_enrollment.create_enrollment(db, student_id=current_user.id, course_id=enrollment_in.course_id)
    return enrollment

# ----------------- Endpoint para OBTENER los estudiantes inscritos en un curso (Para Docentes) -----------------
@router.post("/admin", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def admin_enroll_student(
    student_id: int = Query(..., description="ID del estudiante a inscribir"),
    course_id: int = Query(..., description="ID del curso"),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Permite a un administrador inscribir cualquier estudiante en un curso.
    """
    if current_user.rol != UserRole.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden inscribir estudiantes."
        )
    
    # Verificar que el estudiante existe y es estudiante
    from app.crud import crud_user
    student = crud_user.get_user_by_id(db, user_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.rol != UserRole.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario especificado no es un estudiante"
        )
    
    # Verificar que el curso existe
    course = crud_course.get_course_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar si ya está inscrito
    existing = crud_enrollment.get_enrollment_by_user_and_course(
        db, student_id=student_id, course_id=course_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante ya está inscrito en este curso"
        )
    
    # Crear la inscripción
    enrollment = crud_enrollment.create_enrollment(
        db, student_id=student_id, course_id=course_id
    )
    
    return enrollment


@router.get("/course/{course_id}/students", response_model=List[Any])
async def read_students_in_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Obtiene la lista de estudiantes inscritos en un curso específico.
    Solo el docente propietario del curso o un admin pueden ver esto.
    """
    course = crud_course.get_course_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    
    # Verificar permisos: solo el docente propietario o admin
    if current_user.rol != UserRole.ADMINISTRADOR and current_user.id != course.propietario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los estudiantes de este curso"
        )
    
    students = crud_enrollment.get_students_enrolled_in_course(db, course_id=course_id)
    
    # Formatear la respuesta con información relevante del estudiante
    from app.schemas.user import User as UserSchema
    result = []
    for student in students:
        result.append({
            "id": student.id,
            "full_name": student.nombre_completo,
            "email": student.correo,
            "role": student.rol.value if hasattr(student.rol, 'value') else str(student.rol)
        })
    
    return result

# ----------------- Endpoint para ELIMINAR a un estudiante de un curso (Admin/Docente) -----------------
@router.delete("/course/{course_id}/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_student_from_course(
    course_id: int,
    student_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Elimina (da de baja) a un estudiante de un curso específico.
    Acceso: Administrador o Docente propietario del curso.
    """
    course = crud_course.get_course_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    
    # Verificar permisos: Admin o Propietario
    if current_user.rol != UserRole.ADMINISTRADOR and current_user.id != course.propietario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar estudiantes de este curso"
        )
    
    # Verificar si existe la inscripción
    enrollment = crud_enrollment.get_enrollment_by_user_and_course(
        db, student_id=student_id, course_id=course_id
    )
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estudiante no está inscrito en este curso"
        )
    
    # Eliminar
    crud_enrollment.delete_enrollment(db, db_enrollment=enrollment)
    
    return None