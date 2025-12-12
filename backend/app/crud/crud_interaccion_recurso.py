# backend/app/crud/crud_interaccion_recurso.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.interaccion_recurso import InteraccionRecurso
from app.schemas.interaccion_recurso import InteraccionRecursoCreate, InteraccionRecursoUpdate

# ----------------- Crear una interacción -----------------
def create_interaccion(db: Session, interaccion_in: InteraccionRecursoCreate) -> InteraccionRecurso:
    """
    Crea una nueva interacción de un estudiante con un recurso.
    """
    db_interaccion = InteraccionRecurso(
        estudiante_id=interaccion_in.estudiante_id,
        recurso_id=interaccion_in.recurso_id,
        tipo_interaccion=interaccion_in.tipo_interaccion,
        calificacion=interaccion_in.calificacion,
        tiempo_visto_segundos=interaccion_in.tiempo_visto_segundos,
        mejora_nota=interaccion_in.mejora_nota or False
    )
    db.add(db_interaccion)
    db.commit()
    db.refresh(db_interaccion)
    return db_interaccion

# ----------------- Obtener una interacción por ID -----------------
def get_interaccion_by_id(db: Session, interaccion_id: int) -> Optional[InteraccionRecurso]:
    """
    Obtiene una interacción específica por su ID.
    """
    return db.query(InteraccionRecurso).filter(InteraccionRecurso.id == interaccion_id).first()

# ----------------- Obtener interacciones de un estudiante -----------------
def get_interacciones_by_estudiante(db: Session, estudiante_id: int, skip: int = 0, limit: int = 100) -> List[InteraccionRecurso]:
    """
    Obtiene todas las interacciones de un estudiante.
    """
    return db.query(InteraccionRecurso).filter(
        InteraccionRecurso.estudiante_id == estudiante_id
    ).order_by(InteraccionRecurso.fecha_interaccion.desc()).offset(skip).limit(limit).all()

# ----------------- Obtener interacciones de un recurso -----------------
def get_interacciones_by_recurso(db: Session, recurso_id: int, skip: int = 0, limit: int = 100) -> List[InteraccionRecurso]:
    """
    Obtiene todas las interacciones de un recurso.
    """
    return db.query(InteraccionRecurso).filter(
        InteraccionRecurso.recurso_id == recurso_id
    ).order_by(InteraccionRecurso.fecha_interaccion.desc()).offset(skip).limit(limit).all()

# ----------------- Obtener interacciones por tipo -----------------
def get_interacciones_by_tipo(db: Session, tipo_interaccion: str, skip: int = 0, limit: int = 100) -> List[InteraccionRecurso]:
    """
    Obtiene todas las interacciones de un tipo específico.
    """
    return db.query(InteraccionRecurso).filter(
        InteraccionRecurso.tipo_interaccion == tipo_interaccion
    ).order_by(InteraccionRecurso.fecha_interaccion.desc()).offset(skip).limit(limit).all()

# ----------------- Actualizar una interacción -----------------
def update_interaccion(db: Session, db_interaccion: InteraccionRecurso, interaccion_in: InteraccionRecursoUpdate) -> InteraccionRecurso:
    """
    Actualiza una interacción existente.
    """
    update_data = interaccion_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_interaccion, field, value)
    
    db.add(db_interaccion)
    db.commit()
    db.refresh(db_interaccion)
    return db_interaccion

# ----------------- Eliminar una interacción -----------------
def delete_interaccion(db: Session, interaccion_id: int) -> Optional[InteraccionRecurso]:
    """
    Elimina una interacción específica por su ID.
    """
    db_interaccion = db.query(InteraccionRecurso).filter(InteraccionRecurso.id == interaccion_id).first()
    if db_interaccion:
        db.delete(db_interaccion)
        db.commit()
    return db_interaccion

# ----------------- Obtener estadísticas de un recurso -----------------
def get_recurso_stats(db: Session, recurso_id: int) -> dict:
    """
    Obtiene estadísticas de interacciones de un recurso.
    """
    interacciones = db.query(InteraccionRecurso).filter(InteraccionRecurso.recurso_id == recurso_id).all()
    
    total_views = sum(1 for i in interacciones if i.tipo_interaccion == "viewed")
    total_completions = sum(1 for i in interacciones if i.tipo_interaccion == "completed")
    total_ratings = sum(1 for i in interacciones if i.tipo_interaccion == "rated")
    avg_rating = sum(i.calificacion for i in interacciones if i.calificacion) / total_ratings if total_ratings > 0 else 0
    total_mejoras = sum(1 for i in interacciones if i.mejora_nota)
    
    return {
        "total_interacciones": len(interacciones),
        "total_views": total_views,
        "total_completions": total_completions,
        "total_ratings": total_ratings,
        "avg_rating": round(avg_rating, 2) if total_ratings > 0 else None,
        "total_mejoras": total_mejoras
    }




