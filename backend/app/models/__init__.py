# backend/app/models/__init__.py
# Importa todos los modelos aquí para que sean accesibles a través de 'from app.models import ...'

from .user import User
from .course import Course
from .enrollment import Enrollment
from .task import Task
from .submission import Submission
from .announcement import Announcement
from .comment import Comment
from .student_profile import StudentProfile
from .exam import Exam, ExamSubmission
from .exam_question import ExamQuestion, QuestionOption, QuestionType

# Modelos para el Sistema de Recomendación de Contenido Remedial
from .concepto import Concepto
from .recurso import Recurso
from .tarea_concepto import TareaConcepto
from .recurso_concepto import RecursoConcepto
from .recomendacion_estudiante import RecomendacionEstudiante
from .interaccion_recurso import InteraccionRecurso