# backend/app/crud/crud_recomendacion_estudiante.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.models.recomendacion_estudiante import RecomendacionEstudiante
from app.schemas.recomendacion_estudiante import RecomendacionEstudianteCreate, RecomendacionEstudianteUpdate

# ----------------- Crear una recomendación -----------------
def create_recomendacion(db: Session, recomendacion_in: RecomendacionEstudianteCreate) -> RecomendacionEstudiante:
    """
    Crea una nueva recomendación para un estudiante.
    """
    # Verificar si ya existe esta recomendación
    existing = db.query(RecomendacionEstudiante).filter(
        RecomendacionEstudiante.estudiante_id == recomendacion_in.estudiante_id,
        RecomendacionEstudiante.tarea_id == recomendacion_in.tarea_id,
        RecomendacionEstudiante.recurso_id == recomendacion_in.recurso_id
    ).first()
    
    if existing:
        return existing  # No crear duplicados
    
    db_recomendacion = RecomendacionEstudiante(
        estudiante_id=recomendacion_in.estudiante_id,
        tarea_id=recomendacion_in.tarea_id,
        recurso_id=recomendacion_in.recurso_id
    )
    db.add(db_recomendacion)
    db.commit()
    db.refresh(db_recomendacion)
    return db_recomendacion

# ----------------- Obtener una recomendación por ID -----------------
def get_recomendacion_by_id(db: Session, recomendacion_id: int) -> Optional[RecomendacionEstudiante]:
    """
    Obtiene una recomendación específica por su ID.
    """
    return db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.id == recomendacion_id).first()

# ----------------- Obtener recomendaciones de un estudiante -----------------
def get_recomendaciones_by_estudiante(db: Session, estudiante_id: int, solo_no_vistas: bool = False) -> List[RecomendacionEstudiante]:
    """
    Obtiene todas las recomendaciones de un estudiante.
    Si solo_no_vistas es True, solo retorna recomendaciones no vistas.
    """
    query = db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.estudiante_id == estudiante_id)
    if solo_no_vistas:
        query = query.filter(RecomendacionEstudiante.vista == False)
    return query.order_by(RecomendacionEstudiante.fecha_recomendacion.desc()).all()

# ----------------- Obtener recomendaciones de una tarea -----------------
def get_recomendaciones_by_tarea(db: Session, tarea_id: int) -> List[RecomendacionEstudiante]:
    """
    Obtiene todas las recomendaciones asociadas a una tarea.
    """
    return db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.tarea_id == tarea_id).all()

# ----------------- Marcar recomendación como vista -----------------
def mark_recomendacion_as_viewed(db: Session, recomendacion_id: int) -> Optional[RecomendacionEstudiante]:
    """
    Marca una recomendación como vista y actualiza la fecha de vista.
    """
    db_recomendacion = db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.id == recomendacion_id).first()
    if db_recomendacion:
        db_recomendacion.vista = True
        db_recomendacion.fecha_vista = datetime.now(timezone.utc)
        db.add(db_recomendacion)
        db.commit()
        db.refresh(db_recomendacion)
    return db_recomendacion

# ----------------- Actualizar una recomendación -----------------
def update_recomendacion(db: Session, db_recomendacion: RecomendacionEstudiante, recomendacion_in: RecomendacionEstudianteUpdate) -> RecomendacionEstudiante:
    """
    Actualiza una recomendación existente.
    """
    update_data = recomendacion_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_recomendacion, field, value)
    
    # Si se marca como vista y no tiene fecha_vista, establecerla
    if db_recomendacion.vista and not db_recomendacion.fecha_vista:
        db_recomendacion.fecha_vista = datetime.now(timezone.utc)
    
    db.add(db_recomendacion)
    db.commit()
    db.refresh(db_recomendacion)
    return db_recomendacion

# ----------------- Eliminar una recomendación -----------------
def delete_recomendacion(db: Session, recomendacion_id: int) -> Optional[RecomendacionEstudiante]:
    """
    Elimina una recomendación específica por su ID.
    """
    db_recomendacion = db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.id == recomendacion_id).first()
    if db_recomendacion:
        db.delete(db_recomendacion)
        db.commit()
    return db_recomendacion

# ----------------- Eliminar recomendaciones de una tarea -----------------
def delete_recomendaciones_by_tarea(db: Session, tarea_id: int) -> int:
    """
    Elimina todas las recomendaciones asociadas a una tarea.
    Retorna el número de recomendaciones eliminadas.
    """
    count = db.query(RecomendacionEstudiante).filter(RecomendacionEstudiante.tarea_id == tarea_id).delete()
    db.commit()
    return count




