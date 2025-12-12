# backend/app/crud/crud_recurso.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.recurso import Recurso
from app.schemas.recurso import RecursoCreate, RecursoUpdate

# ----------------- Crear un nuevo recurso -----------------
def create_recurso(db: Session, recurso_in: RecursoCreate) -> Recurso:
    """
    Crea un nuevo recurso en la base de datos.
    """
    db_recurso = Recurso(
        titulo=recurso_in.titulo,
        tipo=recurso_in.tipo,
        url=recurso_in.url,
        ruta_archivo=recurso_in.ruta_archivo,
        descripcion=recurso_in.descripcion,
        duracion_minutos=recurso_in.duracion_minutos,
        nivel_dificultad=recurso_in.nivel_dificultad,
        autor=recurso_in.autor,
        activo=recurso_in.activo
    )
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

# ----------------- Obtener un recurso por ID -----------------
def get_recurso_by_id(db: Session, recurso_id: int) -> Optional[Recurso]:
    """
    Obtiene un recurso específico por su ID.
    """
    return db.query(Recurso).filter(Recurso.id == recurso_id).first()

# ----------------- Obtener todos los recursos -----------------
def get_recursos(db: Session, skip: int = 0, limit: int = 100, solo_activos: bool = True) -> List[Recurso]:
    """
    Obtiene todos los recursos existentes en la base de datos.
    Si solo_activos es True, solo retorna recursos activos.
    """
    query = db.query(Recurso)
    if solo_activos:
        query = query.filter(Recurso.activo == True)
    return query.offset(skip).limit(limit).all()

# ----------------- Obtener recursos por tipo -----------------
def get_recursos_by_tipo(db: Session, tipo: str, skip: int = 0, limit: int = 100, solo_activos: bool = True) -> List[Recurso]:
    """
    Obtiene todos los recursos de un tipo específico.
    """
    query = db.query(Recurso).filter(Recurso.tipo == tipo)
    if solo_activos:
        query = query.filter(Recurso.activo == True)
    return query.offset(skip).limit(limit).all()

# ----------------- Obtener recursos por nivel de dificultad -----------------
def get_recursos_by_nivel_dificultad(db: Session, nivel: str, skip: int = 0, limit: int = 100, solo_activos: bool = True) -> List[Recurso]:
    """
    Obtiene todos los recursos de un nivel de dificultad específico.
    """
    query = db.query(Recurso).filter(Recurso.nivel_dificultad == nivel)
    if solo_activos:
        query = query.filter(Recurso.activo == True)
    return query.offset(skip).limit(limit).all()

# ----------------- Actualizar un recurso -----------------
def update_recurso(db: Session, db_recurso: Recurso, recurso_in: RecursoUpdate) -> Recurso:
    """
    Actualiza un recurso existente en la base de datos.
    """
    update_data = recurso_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_recurso, field, value)
    
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

# ----------------- Eliminar un recurso -----------------
def delete_recurso(db: Session, recurso_id: int) -> Optional[Recurso]:
    """
    Elimina un recurso específico por su ID.
    """
    db_recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    if db_recurso:
        db.delete(db_recurso)
        db.commit()
    return db_recurso

# ----------------- Activar/Desactivar un recurso -----------------
def toggle_recurso_activo(db: Session, recurso_id: int) -> Optional[Recurso]:
    """
    Activa o desactiva un recurso (soft delete).
    """
    db_recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    if db_recurso:
        db_recurso.activo = not db_recurso.activo
        db.add(db_recurso)
        db.commit()
        db.refresh(db_recurso)
    return db_recurso

# ----------------- Obtener recursos por categorías de conceptos -----------------
def get_recursos_by_categorias_conceptos(db: Session, categorias: List[str], skip: int = 0, limit: int = 100, solo_activos: bool = True) -> List[Recurso]:
    """
    Obtiene todos los recursos que están asociados a conceptos que pertenecen
    a alguna de las categorías especificadas.
    """
    from app.models.concepto import Concepto
    from app.models.recurso_concepto import RecursoConcepto
    
    if not categorias:
        return []
    
    query = db.query(Recurso).distinct().join(
        RecursoConcepto, RecursoConcepto.recurso_id == Recurso.id
    ).join(
        Concepto, Concepto.id == RecursoConcepto.concepto_id
    ).filter(
        Concepto.categoria.in_(categorias)
    )
    
    if solo_activos:
        query = query.filter(Recurso.activo == True)
    
    return query.offset(skip).limit(limit).all()


