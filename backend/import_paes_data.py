"""
Script para importar datos históricos desde CSV y adaptar la plataforma
para ser preuniversitaria con temáticas PAES
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.db.base import Base
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.task import Task
from app.models.submission import Submission
from app.models.student_profile import StudentProfile
from app.core.security import get_password_hash

# Crear engine y sesión
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Temáticas PAES para cursos preuniversitarios (adaptadas a los IDs del CSV)
PAES_COURSES = {
    1: {
        "title": "Lenguaje y Comunicación - PAES",
        "description": "Preparación para la prueba de Lenguaje y Comunicación. Comprensión lectora, análisis textual, ortografía y gramática."
    },
    2: {
        "title": "Matemáticas PAES - Competencia M1",
        "description": "Preparación para Competencia Matemática M1. Álgebra, funciones, geometría y probabilidades básicas."
    },
    3: {
        "title": "Matemáticas PAES - Competencia M2",
        "description": "Preparación para Competencia Matemática M2. Cálculo, trigonometría avanzada y geometría analítica."
    },
    4: {
        "title": "Historia y Ciencias Sociales - PAES",
        "description": "Preparación para la prueba de Historia y Ciencias Sociales. Historia de Chile, historia universal y geografía."
    },
    5: {
        "title": "Ciencias - Biología PAES",
        "description": "Preparación para la prueba de Ciencias - Biología. Celular, genética, evolución y ecología."
    }
}

# Docentes especializados en áreas PAES
PAES_TEACHERS = [
    {
        "first_name": "Patricia",
        "last_name": "Morales",
        "email": "patricia.morales@paes.cl",
        "specialization": "Lenguaje y Comunicación"
    },
    {
        "first_name": "Roberto",
        "last_name": "González",
        "email": "roberto.gonzalez@paes.cl",
        "specialization": "Matemáticas"
    },
    {
        "first_name": "María",
        "last_name": "Vega",
        "email": "maria.vega@paes.cl",
        "specialization": "Ciencias"
    },
    {
        "first_name": "Carlos",
        "last_name": "Fernández",
        "email": "carlos.fernandez@paes.cl",
        "specialization": "Historia"
    },
]

def clear_existing_data(db: Session):
    """Limpia datos existentes (mantiene usuarios administrativos)"""
    print("Limpiando datos existentes...")
    
    # Eliminar en orden para respetar foreign keys
    db.query(Submission).delete()
    db.query(Task).delete()
    db.query(Comment).delete()
    db.query(Announcement).delete()
    db.query(Enrollment).delete()
    db.query(StudentProfile).delete()
    db.query(Course).delete()
    
    # Eliminar usuarios no administrativos
    db.query(User).filter(User.role != UserRole.ADMINISTRADOR).delete()
    
    db.commit()
    print("✅ Datos limpiados")

def create_paes_teachers(db: Session):
    """Crea docentes especializados en áreas PAES"""
    print("Creando docentes PAES...")
    
    teachers = []
    for teacher_data in PAES_TEACHERS:
        existing = db.query(User).filter(User.email == teacher_data["email"]).first()
        if not existing:
            teacher = User(
                email=teacher_data["email"],
                full_name=f"{teacher_data['first_name']} {teacher_data['last_name']}",
                hashed_password=get_password_hash("paes2024"),
                role=UserRole.DOCENTE,
                is_active=True
            )
            db.add(teacher)
            teachers.append(teacher)
        else:
            existing.role = UserRole.DOCENTE
            existing.is_active = True
            teachers.append(existing)
    
    db.commit()
    for teacher in teachers:
        db.refresh(teacher)
    
    print(f"✅ Creados/actualizados {len(teachers)} docentes PAES")
    return teachers

def create_paes_courses(db: Session, teachers):
    """Crea cursos PAES"""
    print("Creando cursos PAES...")
    
    # Mapear docentes a cursos por especialización
    teacher_by_specialization = {
        "Lenguaje": next((t for t in teachers if "Lenguaje" in t.full_name or "patricia" in t.email.lower()), teachers[0]),
        "Matemáticas": next((t for t in teachers if "Matemáticas" in t.full_name or "roberto" in t.email.lower()), teachers[1]),
        "Ciencias": next((t for t in teachers if "Ciencias" in t.full_name or "maria" in t.email.lower()), teachers[2]),
        "Historia": next((t for t in teachers if "Historia" in t.full_name or "carlos" in t.email.lower()), teachers[3] if len(teachers) > 3 else teachers[0]),
    }
    
    courses_map = {}  # Mapeo course_id del CSV -> Course objeto
    
    for course_id, course_data in PAES_COURSES.items():
        # Verificar si el curso ya existe
        existing_course = db.query(Course).filter(Course.id == course_id).first()
        
        # Determinar docente según el curso
        if "Lenguaje" in course_data["title"] or "Competencia Lectora" in course_data["title"]:
            owner = teacher_by_specialization["Lenguaje"]
        elif "Matemática" in course_data["title"]:
            owner = teacher_by_specialization["Matemáticas"]
        elif "Ciencias" in course_data["title"] or "Biología" in course_data["title"] or "Física" in course_data["title"] or "Química" in course_data["title"]:
            owner = teacher_by_specialization["Ciencias"]
        elif "Historia" in course_data["title"]:
            owner = teacher_by_specialization["Historia"]
        else:
            owner = teachers[0]
        
        if existing_course:
            # Actualizar curso existente
            existing_course.title = course_data["title"]
            existing_course.description = course_data["description"]
            existing_course.owner_id = owner.id
            courses_map[course_id] = existing_course
        else:
            # Crear nuevo curso
            course = Course(
                id=course_id,  # Mantener el mismo ID del CSV
                title=course_data["title"],
                description=course_data["description"],
                owner_id=owner.id,
                created_at=datetime.now(timezone.utc) - pd.Timedelta(days=120)
            )
            db.add(course)
            courses_map[course_id] = course
    
    db.commit()
    for course in courses_map.values():
        db.refresh(course)
    
    print(f"✅ Creados {len(courses_map)} cursos PAES")
    return courses_map

def import_from_csv(db: Session, csv_path: str, courses_map):
    """Importa datos desde el CSV histórico"""
    print(f"Leyendo CSV: {csv_path}...")
    
    df = pd.read_csv(csv_path)
    print(f"Total registros en CSV: {len(df)}")
    
    # Convertir fechas (usar formato ISO8601 para manejar timezone)
    df['due_date'] = pd.to_datetime(df['due_date'], format='ISO8601', errors='coerce')
    df['task_created_at'] = pd.to_datetime(df['task_created_at'], format='ISO8601', errors='coerce')
    df['enrollment_date'] = pd.to_datetime(df['enrollment_date'], format='ISO8601', errors='coerce')
    df['submitted_at'] = pd.to_datetime(df['submitted_at'], format='ISO8601', errors='coerce')
    
    # Crear estudiantes únicos (convertir a int de Python)
    student_ids = sorted([int(sid) for sid in df['student_id'].unique()])
    print(f"Estudiantes únicos: {len(student_ids)}")
    
    students_map = {}
    for student_id in student_ids:
        student_data = df[df['student_id'] == student_id].iloc[0]
        
        existing = db.query(User).filter(User.id == student_id).first()
        if not existing:
            student = User(
                id=student_id,  # Mantener ID del CSV
                email=f"estudiante{student_id}@paes.cl",
                full_name=f"Estudiante {student_id}",
                hashed_password=get_password_hash("paes2024"),
                role=UserRole.ESTUDIANTE,
                is_active=True
            )
            db.add(student)
            students_map[student_id] = student
        else:
            existing.role = UserRole.ESTUDIANTE
            existing.is_active = True
            students_map[student_id] = existing
    
    db.commit()
    for student in students_map.values():
        db.refresh(student)
    
    print(f"✅ Creados/actualizados {len(students_map)} estudiantes")
    
    # Crear inscripciones (convertir IDs a int)
    enrollments_created = 0
    enrollment_pairs = df[['student_id', 'course_id', 'enrollment_date']].drop_duplicates()
    
    for _, row in enrollment_pairs.iterrows():
        student_id = int(float(row['student_id']))
        course_id = int(float(row['course_id']))
        enrollment_date = row['enrollment_date']
        
        if student_id not in students_map or course_id not in courses_map:
            continue
        
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()
        
        if not existing:
            enrollment = Enrollment(
                student_id=student_id,
                course_id=course_id,
                enrollment_date=enrollment_date.to_pydatetime().replace(tzinfo=timezone.utc) if pd.notna(enrollment_date) else datetime.now(timezone.utc)
            )
            db.add(enrollment)
            enrollments_created += 1
    
    db.commit()
    print(f"✅ Creadas {enrollments_created} inscripciones")
    
    # Crear tareas (usar drop_duplicates correctamente)
    tasks_map = {}
    task_data = df[['task_id', 'course_id', 'due_date', 'task_created_at']].drop_duplicates(subset=['task_id'], keep='first')
    
    print(f"Tareas únicas a crear: {len(task_data)}")
    
    # Generar títulos de tareas según el curso
    task_titles = {
        1: ["Comprensión Lectora I", "Análisis Textual", "Ortografía y Gramática", "Ensayo Argumentativo", "Literatura Chilena"],
        2: ["Álgebra Básica", "Funciones Lineales", "Geometría Plana", "Probabilidades", "Ejercicios Integrados M1"],
        3: ["Cálculo Diferencial", "Trigonometría Avanzada", "Geometría Analítica", "Funciones Exponenciales", "Ejercicios Integrados M2"],
        4: ["Historia de Chile - Colonia", "Historia Universal - Edad Media", "Geografía Física", "Historia del Siglo XX", "Síntesis Histórica"],
        5: ["Célula y Organización", "Genética y Herencia", "Evolución", "Ecología y Ecosistemas", "Biología Integrada"]
    }
    
    # Contar tareas por curso para asignar títulos
    task_counts = {}
    
    for _, row in task_data.iterrows():
        task_id = int(float(row['task_id']))
        course_id = int(float(row['course_id']))
        
        if course_id not in courses_map:
            continue
        
        if course_id not in task_counts:
            task_counts[course_id] = 0
        
        existing = db.query(Task).filter(Task.id == task_id).first()
        if not existing:
            # Asignar título según el curso
            task_index = task_counts[course_id] % 5
            title = task_titles.get(course_id, [f"Tarea {task_id}"])[task_index] if course_id in task_titles else f"Tarea {task_id} - PAES"
            task_counts[course_id] += 1
            
            due_date_val = row['due_date']
            created_at_val = row['task_created_at']
            
            task = Task(
                id=task_id,
                title=title,
                description=f"Ejercicios y práctica para preparación PAES - {title}",
                due_date=due_date_val.to_pydatetime().replace(tzinfo=timezone.utc) if pd.notna(due_date_val) else datetime.now(timezone.utc),
                course_id=course_id,
                created_at=created_at_val.to_pydatetime().replace(tzinfo=timezone.utc) if pd.notna(created_at_val) else datetime.now(timezone.utc)
            )
            db.add(task)
            tasks_map[task_id] = task
        else:
            tasks_map[task_id] = existing
    
    db.commit()
    for task in tasks_map.values():
        db.refresh(task)
    
    print(f"✅ Creadas {len(tasks_map)} tareas")
    
    # Crear entregas y calificaciones
    submissions_created = 0
    for _, row in df.iterrows():
        if pd.isna(row['submission_id']):
            continue
        
        student_id = int(float(row['student_id']))
        task_id = int(float(row['task_id']))
        submission_id = int(float(row['submission_id']))
        
        if student_id not in students_map or task_id not in tasks_map:
            continue
        
        existing = db.query(Submission).filter(Submission.id == submission_id).first()
        if not existing:
            submission = Submission(
                id=submission_id,
                student_id=student_id,
                task_id=task_id,
                content=f"Entrega de estudiante {student_id} para tarea {task_id}",
                file_path=None,
                grade=float(row['grade']) if pd.notna(row['grade']) else None,
                feedback=f"Calificación: {row['grade']}/7.0" if pd.notna(row['grade']) else None,
                submitted_at=row['submitted_at'].to_pydatetime().replace(tzinfo=timezone.utc) if pd.notna(row['submitted_at']) else datetime.now(timezone.utc)
            )
            db.add(submission)
            submissions_created += 1
    
    db.commit()
    print(f"✅ Creadas {submissions_created} entregas")
    
    # Crear perfiles de estudiantes
    profiles_created = 0
    student_profiles = df[['student_id', 'motivation', 'available_time', 'sleep_hours', 'study_hours', 
                          'enjoyment_studying', 'study_place_tranquility', 'academic_pressure', 'gender']].drop_duplicates(subset=['student_id'])
    
    for _, row in student_profiles.iterrows():
        student_id = int(float(row['student_id']))
        
        if student_id not in students_map:
            continue
        
        existing = db.query(StudentProfile).filter(StudentProfile.student_id == student_id).first()
        if not existing:
            profile = StudentProfile(
                student_id=student_id,
                motivation=float(row['motivation']) if pd.notna(row['motivation']) else 5.0,
                available_time=float(row['available_time']) if pd.notna(row['available_time']) else 5.0,
                sleep_hours=float(row['sleep_hours']) if pd.notna(row['sleep_hours']) else 7.0,
                study_hours=float(row['study_hours']) if pd.notna(row['study_hours']) else 5.0,
                enjoyment_studying=float(row['enjoyment_studying']) if pd.notna(row['enjoyment_studying']) else 5.0,
                study_place_tranquility=float(row['study_place_tranquility']) if pd.notna(row['study_place_tranquility']) else 5.0,
                academic_pressure=float(row['academic_pressure']) if pd.notna(row['academic_pressure']) else 5.0,
                gender=str(row['gender']) if pd.notna(row['gender']) else 'otro'
            )
            db.add(profile)
            profiles_created += 1
    
    db.commit()
    print(f"✅ Creados {profiles_created} perfiles de estudiantes")
    
    return students_map, tasks_map

def main():
    """Función principal"""
    print("=" * 70)
    print("IMPORTACIÓN DE DATOS HISTÓRICOS PAES")
    print("=" * 70)
    print()
    
    csv_path = Path(__file__).parent.parent / "datasets" / "historical_dataset_with_profiles.csv"
    
    if not csv_path.exists():
        print(f"❌ Error: No se encuentra el archivo {csv_path}")
        return
    
    db = SessionLocal()
    
    try:
        # 1. Limpiar datos existentes (opcional - comentar si quieres mantener datos)
        # clear_existing_data(db)
        
        # 2. Crear docentes PAES
        teachers = create_paes_teachers(db)
        print()
        
        # 3. Crear cursos PAES
        courses_map = create_paes_courses(db, teachers)
        print()
        
        # 4. Importar datos del CSV
        students_map, tasks_map = import_from_csv(db, str(csv_path), courses_map)
        print()
        
        print("=" * 70)
        print("✅ IMPORTACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print()
        print("Resumen:")
        print(f"  - Docentes PAES: {len(teachers)}")
        print(f"  - Cursos PAES: {len(courses_map)}")
        print(f"  - Estudiantes: {len(students_map)}")
        print(f"  - Tareas: {len(tasks_map)}")
        print()
        print("Credenciales de acceso:")
        print("  Docentes: email del docente / paes2024")
        print("  Estudiantes: estudiante{id}@paes.cl / paes2024")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Importar modelos necesarios
    from app.models.announcement import Announcement
    from app.models.comment import Comment
    
    main()

