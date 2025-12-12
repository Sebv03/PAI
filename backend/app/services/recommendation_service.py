# backend/app/services/recommendation_service.py
"""
Servicio de Recomendación de Contenido Remedial - Nivel 1: Motor Basado en Reglas
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.models.recomendacion_estudiante import RecomendacionEstudiante
from app.models.recurso import Recurso
from app.models.tarea_concepto import TareaConcepto
from app.models.recurso_concepto import RecursoConcepto
from app.crud import crud_task, crud_recomendacion_estudiante
from app.schemas.recomendacion_estudiante import RecomendacionEstudianteCreate

class RecommendationService:
    """
    Servicio para generar recomendaciones de recursos remediales basado en reglas.
    Nivel 1: Motor Basado en Reglas (MVP)
    
    Lógica:
    1. Detecta nota baja (por defecto < 4.0)
    2. Obtiene conceptos de la tarea fallida
    3. Busca recursos que cubran esos conceptos
    4. Genera recomendaciones para el estudiante
    """
    
    def __init__(self, db: Session, umbral_nota: float = 4.0):
        """
        Inicializa el servicio de recomendaciones.
        
        Args:
            db: Sesión de base de datos
            umbral_nota: Nota mínima para considerar "baja" (default: 4.0)
        """
        self.db = db
        self.umbral_nota = umbral_nota
        self.max_recomendaciones = 3  # Número máximo de recursos a recomendar
    
    def generate_recommendations_for_low_grade(
        self,
        estudiante_id: int,
        tarea_id: int,
        nota: float
    ) -> List[Recurso]:
        """
        Genera recomendaciones de recursos cuando un estudiante obtiene una nota baja.
        
        Args:
            estudiante_id: ID del estudiante
            tarea_id: ID de la tarea calificada
            nota: Nota obtenida (1.0 a 7.0)
        
        Returns:
            Lista de recursos recomendados
        """
        # Si la nota es mayor o igual al umbral, no generar recomendaciones
        if nota >= self.umbral_nota:
            return []
        
        # 1. Obtener conceptos asociados a la tarea
        conceptos_ids = self._get_conceptos_from_tarea(tarea_id)
        
        if not conceptos_ids:
            print(f"⚠️  La tarea {tarea_id} no tiene conceptos asociados. No se pueden generar recomendaciones.")
            return []
        
        # 2. Buscar recursos que cubran esos conceptos
        recursos = self._find_recursos_by_conceptos(conceptos_ids)
        
        if not recursos:
            print(f"⚠️  No se encontraron recursos para los conceptos de la tarea {tarea_id}.")
            return []
        
        # 3. Filtrar recursos ya recomendados para esta tarea (evitar duplicados)
        recursos_filtrados = self._filter_existing_recommendations(
            estudiante_id, tarea_id, recursos
        )
        
        # 4. Priorizar recursos (por ahora, por número de conceptos coincidentes y nivel básico)
        recursos_priorizados = self._priorize_recursos(recursos_filtrados, conceptos_ids)
        
        # 5. Limitar número de recomendaciones
        recursos_finales = recursos_priorizados[:self.max_recomendaciones]
        
        # 6. Crear registros de recomendaciones
        recomendaciones_creadas = []
        for recurso in recursos_finales:
            try:
                recomendacion_in = RecomendacionEstudianteCreate(
                    estudiante_id=estudiante_id,
                    tarea_id=tarea_id,
                    recurso_id=recurso.id
                )
                recomendacion = crud_recomendacion_estudiante.create_recomendacion(
                    db=self.db,
                    recomendacion_in=recomendacion_in
                )
                recomendaciones_creadas.append(recomendacion)
            except Exception as e:
                print(f"⚠️  Error al crear recomendación para recurso {recurso.id}: {e}")
                # Continuar con los demás recursos
        
        print(f"✅ Generadas {len(recomendaciones_creadas)} recomendaciones para estudiante {estudiante_id} en tarea {tarea_id}")
        
        return recursos_finales
    
    def _get_conceptos_from_tarea(self, tarea_id: int) -> List[int]:
        """
        Obtiene los IDs de los conceptos asociados a una tarea.
        """
        tarea_conceptos = self.db.query(TareaConcepto).filter(
            TareaConcepto.tarea_id == tarea_id
        ).all()
        
        return [tc.concepto_id for tc in tarea_conceptos]
    
    def _find_recursos_by_conceptos(self, conceptos_ids: List[int]) -> List[Recurso]:
        """
        Busca recursos que cubran al menos uno de los conceptos dados.
        Solo retorna recursos activos.
        """
        # Buscar recursos que tengan al menos uno de los conceptos
        recursos_conceptos = self.db.query(RecursoConcepto).join(Recurso).filter(
            RecursoConcepto.concepto_id.in_(conceptos_ids),
            Recurso.activo == True
        ).distinct().all()
        
        # Obtener los IDs de recursos únicos
        recurso_ids = list(set([rc.recurso_id for rc in recursos_conceptos]))
        
        # Obtener los objetos Recurso
        recursos = self.db.query(Recurso).filter(
            Recurso.id.in_(recurso_ids),
            Recurso.activo == True
        ).all()
        
        return recursos
    
    def _filter_existing_recommendations(
        self,
        estudiante_id: int,
        tarea_id: int,
        recursos: List[Recurso]
    ) -> List[Recurso]:
        """
        Filtra recursos que ya fueron recomendados para esta tarea.
        """
        # Obtener recomendaciones existentes para esta tarea y estudiante
        recomendaciones_existentes = self.db.query(RecomendacionEstudiante).filter(
            RecomendacionEstudiante.estudiante_id == estudiante_id,
            RecomendacionEstudiante.tarea_id == tarea_id
        ).all()
        
        recurso_ids_recomendados = {rec.recurso_id for rec in recomendaciones_existentes}
        
        # Filtrar recursos ya recomendados
        recursos_filtrados = [
            r for r in recursos
            if r.id not in recurso_ids_recomendados
        ]
        
        return recursos_filtrados
    
    def _priorize_recursos(
        self,
        recursos: List[Recurso],
        conceptos_ids: List[int]
    ) -> List[Recurso]:
        """
        Prioriza recursos según:
        1. Número de conceptos coincidentes (más es mejor)
        2. Nivel de dificultad (básico primero)
        3. Duración (más cortos primero)
        """
        def calcular_score(recurso: Recurso) -> tuple:
            # 1. Contar conceptos coincidentes
            recursos_conceptos = self.db.query(RecursoConcepto).filter(
                RecursoConcepto.recurso_id == recurso.id,
                RecursoConcepto.concepto_id.in_(conceptos_ids)
            ).all()
            
            num_conceptos = len(recursos_conceptos)
            
            # 2. Score por nivel de dificultad (básico = 3, intermedio = 2, avanzado = 1)
            nivel_scores = {
                "básico": 3,
                "intermedio": 2,
                "avanzado": 1
            }
            nivel_score = nivel_scores.get(recurso.nivel_dificultad, 0)
            
            # 3. Score por duración (más cortos = mejor, pero invertido para ordenar descendente)
            # Si no tiene duración, usar 0 (se prioriza al final)
            duracion_score = 1000 - (recurso.duracion_minutos or 0)
            
            # Score total: (conceptos, nivel, duración)
            return (-num_conceptos, -nivel_score, -duracion_score)
        
        # Ordenar por score (tuplas se ordenan lexicográficamente)
        recursos_ordenados = sorted(recursos, key=calcular_score)
        
        return recursos_ordenados
    
    def get_recommendations_for_student(
        self,
        estudiante_id: int,
        solo_no_vistas: bool = False
    ) -> List[RecomendacionEstudiante]:
        """
        Obtiene todas las recomendaciones de un estudiante.
        """
        return crud_recomendacion_estudiante.get_recomendaciones_by_estudiante(
            db=self.db,
            estudiante_id=estudiante_id,
            solo_no_vistas=solo_no_vistas
        )

