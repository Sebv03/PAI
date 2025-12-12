# backend/app/crud/crud_recurso_concepto.py
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.models.recurso_concepto import RecursoConcepto
from app.schemas.recurso_concepto import RecursoConceptoCreate, RecursoConceptosCreate

# ----------------- Crear una relación recurso-concepto -----------------
def create_recurso_concepto(db: Session, recurso_concepto_in: RecursoConceptoCreate) -> RecursoConcepto:
    """
    Crea una nueva relación entre un recurso y un concepto.
    """
    db_recurso_concepto = RecursoConcepto(
        recurso_id=recurso_concepto_in.recurso_id,
        concepto_id=recurso_concepto_in.concepto_id,
        relevancia=Decimal(str(recurso_concepto_in.relevancia)) if recurso_concepto_in.relevancia else Decimal('1.0')
    )
    db.add(db_recurso_concepto)
    db.commit()
    db.refresh(db_recurso_concepto)
    return db_recurso_concepto

# ----------------- Asociar múltiples conceptos a un recurso -----------------
def associate_conceptos_to_recurso(db: Session, recurso_id: int, concepto_ids: List[int], relevancias: Optional[List[float]] = None) -> List[RecursoConcepto]:
    """
    Asocia múltiples conceptos a un recurso.
    Si se proporcionan relevancias, se usan; de lo contrario, se usa 1.0 para todos.
    """
    # Eliminar relaciones existentes para este recurso
    db.query(RecursoConcepto).filter(RecursoConcepto.recurso_id == recurso_id).delete()
    
    # Crear nuevas relaciones
    relaciones = []
    for idx, concepto_id in enumerate(concepto_ids):
        relevancia = Decimal(str(relevancias[idx])) if relevancias and idx < len(relevancias) else Decimal('1.0')
        db_recurso_concepto = RecursoConcepto(
            recurso_id=recurso_id,
            concepto_id=concepto_id,
            relevancia=relevancia
        )
        db.add(db_recurso_concepto)
        relaciones.append(db_recurso_concepto)
    
    db.commit()
    for rel in relaciones:
        db.refresh(rel)
    return relaciones

# ----------------- Obtener conceptos de un recurso -----------------
def get_conceptos_by_recurso(db: Session, recurso_id: int) -> List[RecursoConcepto]:
    """
    Obtiene todos los conceptos asociados a un recurso.
    """
    return db.query(RecursoConcepto).filter(RecursoConcepto.recurso_id == recurso_id).all()

# ----------------- Obtener recursos de un concepto -----------------
def get_recursos_by_concepto(db: Session, concepto_id: int, solo_activos: bool = True) -> List[RecursoConcepto]:
    """
    Obtiene todos los recursos asociados a un concepto.
    Si solo_activos es True, solo retorna recursos activos.
    """
    from app.models.recurso import Recurso
    query = db.query(RecursoConcepto).join(Recurso).filter(RecursoConcepto.concepto_id == concepto_id)
    if solo_activos:
        query = query.filter(Recurso.activo == True)
    return query.all()

# ----------------- Eliminar una relación recurso-concepto -----------------
def delete_recurso_concepto(db: Session, recurso_id: int, concepto_id: int) -> bool:
    """
    Elimina una relación específica entre un recurso y un concepto.
    """
    db_recurso_concepto = db.query(RecursoConcepto).filter(
        RecursoConcepto.recurso_id == recurso_id,
        RecursoConcepto.concepto_id == concepto_id
    ).first()
    if db_recurso_concepto:
        db.delete(db_recurso_concepto)
        db.commit()
        return True
    return False

# ----------------- Eliminar todas las relaciones de un recurso -----------------
def delete_all_recurso_conceptos(db: Session, recurso_id: int) -> int:
    """
    Elimina todas las relaciones de conceptos de un recurso.
    Retorna el número de relaciones eliminadas.
    """
    count = db.query(RecursoConcepto).filter(RecursoConcepto.recurso_id == recurso_id).delete()
    db.commit()
    return count




