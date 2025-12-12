# backend/app/schemas/__init__.py
# Importar schemas del sistema de recomendaciones
from .concepto import Concepto, ConceptoCreate, ConceptoUpdate
from .recurso import Recurso, RecursoCreate, RecursoUpdate, RecursoWithConcepts
from .tarea_concepto import TareaConcepto, TareaConceptoCreate, TareaConceptosCreate
from .recurso_concepto import RecursoConcepto, RecursoConceptoCreate, RecursoConceptosCreate
from .recomendacion_estudiante import RecomendacionEstudiante, RecomendacionEstudianteCreate, RecomendacionEstudianteWithRecurso
from .interaccion_recurso import InteraccionRecurso, InteraccionRecursoCreate




