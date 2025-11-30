"""
Servicio para obtener datos de la base de datos
"""

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import settings


class DataService:
    """Servicio para acceder a los datos de la base de datos"""
    
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    
    def get_historical_data(self) -> pd.DataFrame:
        """
        Obtiene todos los datos históricos necesarios para entrenar el modelo.
        Incluye todas las tareas (entregadas y no entregadas) para calcular correctamente
        la tasa de no entrega.
        También incluye datos del perfil del estudiante (cuestionario).
        Retorna un DataFrame con: student_id, course_id, task_id, due_date, 
        submitted_at, grade, y datos del perfil del estudiante.
        """
        query = text("""
            SELECT 
                t.id as task_id,
                t.curso_id as course_id,
                t.fecha_limite as due_date,
                t.fecha_creacion as task_created_at,
                e.estudiante_id as student_id,
                e.fecha_inscripcion as enrollment_date,
                s.id as submission_id,
                s.fecha_entrega as submitted_at,
                s.calificacion as grade,
                sp.motivacion as motivation,
                sp.tiempo_disponible as available_time,
                sp.horas_sueno as sleep_hours,
                sp.horas_estudio as study_hours,
                sp.disfrute_estudio as enjoyment_studying,
                sp.tranquilidad_lugar_estudio as study_place_tranquility,
                sp.presion_academica as academic_pressure,
                sp.genero as gender
            FROM tasks t
            INNER JOIN enrollments e ON t.curso_id = e.curso_id
            LEFT JOIN submissions s ON s.tarea_id = t.id AND s.estudiante_id = e.estudiante_id
            LEFT JOIN student_profiles sp ON sp.estudiante_id = e.estudiante_id
            ORDER BY e.estudiante_id, t.curso_id, t.fecha_limite
        """)
        
        try:
            df = pd.read_sql(query, self.engine)
            # Normalizar fechas a UTC
            date_columns = ['due_date', 'submitted_at', 'task_created_at', 'enrollment_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True)
                    if df[col].dt.tz is None:
                        df[col] = df[col].dt.tz_localize('UTC')
                    else:
                        df[col] = df[col].dt.tz_convert('UTC')
            return df
        except Exception as e:
            print(f"Error al obtener datos históricos: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_student_course_data(self, student_id: int, course_id: int) -> pd.DataFrame:
        """
        Obtiene los datos de un estudiante específico en un curso específico
        Incluye todas las tareas (entregadas y no entregadas) y datos del perfil
        """
        query = text("""
            SELECT 
                t.id as task_id,
                t.curso_id as course_id,
                t.fecha_limite as due_date,
                t.fecha_creacion as task_created_at,
                e.estudiante_id as student_id,
                e.fecha_inscripcion as enrollment_date,
                s.id as submission_id,
                s.fecha_entrega as submitted_at,
                s.calificacion as grade,
                sp.motivacion as motivation,
                sp.tiempo_disponible as available_time,
                sp.horas_sueno as sleep_hours,
                sp.horas_estudio as study_hours,
                sp.disfrute_estudio as enjoyment_studying,
                sp.tranquilidad_lugar_estudio as study_place_tranquility,
                sp.presion_academica as academic_pressure,
                sp.genero as gender
            FROM tasks t
            INNER JOIN enrollments e ON t.curso_id = e.curso_id
            LEFT JOIN submissions s ON s.tarea_id = t.id AND s.estudiante_id = e.estudiante_id
            LEFT JOIN student_profiles sp ON sp.estudiante_id = e.estudiante_id
            WHERE e.estudiante_id = :student_id 
                AND t.curso_id = :course_id
            ORDER BY t.fecha_limite
        """)
        
        try:
            df = pd.read_sql(
                query, 
                self.engine,
                params={"student_id": student_id, "course_id": course_id}
            )
            # Normalizar fechas a UTC
            date_columns = ['due_date', 'submitted_at', 'task_created_at', 'enrollment_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True)
                    if df[col].dt.tz is None:
                        df[col] = df[col].dt.tz_localize('UTC')
                    else:
                        df[col] = df[col].dt.tz_convert('UTC')
            return df
        except Exception as e:
            print(f"Error al obtener datos del estudiante: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_course_students_data(self, course_id: int) -> pd.DataFrame:
        """
        Obtiene los datos de todos los estudiantes en un curso
        Incluye todas las tareas (entregadas y no entregadas) y datos del perfil
        """
        query = text("""
            SELECT 
                t.id as task_id,
                t.curso_id as course_id,
                t.fecha_limite as due_date,
                t.fecha_creacion as task_created_at,
                e.estudiante_id as student_id,
                e.fecha_inscripcion as enrollment_date,
                s.id as submission_id,
                s.fecha_entrega as submitted_at,
                s.calificacion as grade,
                sp.motivacion as motivation,
                sp.tiempo_disponible as available_time,
                sp.horas_sueno as sleep_hours,
                sp.horas_estudio as study_hours,
                sp.disfrute_estudio as enjoyment_studying,
                sp.tranquilidad_lugar_estudio as study_place_tranquility,
                sp.presion_academica as academic_pressure,
                sp.genero as gender
            FROM tasks t
            INNER JOIN enrollments e ON t.curso_id = e.curso_id
            LEFT JOIN submissions s ON s.tarea_id = t.id AND s.estudiante_id = e.estudiante_id
            LEFT JOIN student_profiles sp ON sp.estudiante_id = e.estudiante_id
            WHERE t.curso_id = :course_id
            ORDER BY e.estudiante_id, t.fecha_limite
        """)
        
        try:
            df = pd.read_sql(
                query,
                self.engine,
                params={"course_id": course_id}
            )
            # Normalizar fechas a UTC
            date_columns = ['due_date', 'submitted_at', 'task_created_at', 'enrollment_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True)
                    if df[col].dt.tz is None:
                        df[col] = df[col].dt.tz_localize('UTC')
                    else:
                        df[col] = df[col].dt.tz_convert('UTC')
            return df
        except Exception as e:
            print(f"Error al obtener datos del curso: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_all_tasks_for_student_course(self, student_id: int, course_id: int) -> pd.DataFrame:
        """
        Obtiene todas las tareas (entregadas y no entregadas) de un estudiante en un curso
        """
        query = text("""
            SELECT 
                t.id as task_id,
                t.course_id,
                t.due_date,
                t.created_at as task_created_at,
                s.id as submission_id,
                s.submitted_at,
                s.grade,
                e.enrollment_date
            FROM tasks t
            INNER JOIN enrollments e ON t.course_id = e.course_id
            LEFT JOIN submissions s ON s.task_id = t.id AND s.student_id = e.student_id
            WHERE e.student_id = :student_id 
                AND t.course_id = :course_id
            ORDER BY t.due_date
        """)
        
        try:
            df = pd.read_sql(
                query,
                self.engine,
                params={"student_id": student_id, "course_id": course_id}
            )
            return df
        except Exception as e:
            print(f"Error al obtener tareas: {e}")
            return pd.DataFrame()

