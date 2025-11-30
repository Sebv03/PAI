"""
Script completo: Limpia datos antiguos e importa datos PAES desde CSV
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.task import Task
from app.models.submission import Submission
from app.models.student_profile import StudentProfile
from app.models.announcement import Announcement
from app.models.comment import Comment
from app.core.security import get_password_hash

# Crear engine y sesión
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Temáticas PAES
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

PAES_TEACHERS = [
    {"first_name": "Patricia", "last_name": "Morales", "email": "patricia.morales@paes.cl", "specialization": "Lenguaje"},
    {"first_name": "Roberto", "last_name": "González", "email": "roberto.gonzalez@paes.cl", "specialization": "Matemáticas"},
    {"first_name": "María", "last_name": "Vega", "email": "maria.vega@paes.cl", "specialization": "Ciencias"},
    {"first_name": "Carlos", "last_name": "Fernández", "email": "carlos.fernandez@paes.cl", "specialization": "Historia"},
]

def clean_all_data(db: Session, keep_admin=True):
    """Limpia todos los datos excepto administradores"""
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
    if keep_admin:
        db.query(User).filter(User.role != UserRole.ADMINISTRADOR).delete()
    else:
        db.query(User).delete()
    
    db.commit()
    print("✅ Datos limpiados")

def main():
    """Ejecuta limpieza e importación"""
    print("=" * 70)
    print("LIMPIEZA E IMPORTACIÓN DE DATOS PAES")
    print("=" * 70)
    print()
    
    csv_path = Path(__file__).parent.parent / "datasets" / "historical_dataset_with_profiles.csv"
    
    if not csv_path.exists():
        print(f"❌ Error: No se encuentra el archivo {csv_path}")
        return
    
    db = SessionLocal()
    
    try:
        # 1. Limpiar datos
        clean_all_data(db, keep_admin=True)
        print()
        
        # 2. Ejecutar script de importación
        print("Ejecutando importación...")
        print()
        
        # Importar funciones del script de importación
        from import_paes_data import (
            create_paes_teachers,
            create_paes_courses,
            import_from_csv
        )
        
        teachers = create_paes_teachers(db)
        print()
        
        courses_map = create_paes_courses(db, teachers)
        print()
        
        students_map, tasks_map = import_from_csv(db, str(csv_path), courses_map)
        print()
        
        print("=" * 70)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        print()
        print("Resumen final:")
        print(f"  - Docentes PAES: {len(teachers)}")
        print(f"  - Cursos PAES: {len(courses_map)}")
        print(f"  - Estudiantes: {len(students_map)}")
        print(f"  - Tareas: {len(tasks_map)}")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()


