# backend/app/crud/crud_tarea_concepto.py
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.models.tarea_concepto import TareaConcepto
from app.models.task import Task
from app.models.concepto import Concepto
from app.schemas.tarea_concepto import TareaConceptoCreate, TareaConceptosCreate

# ----------------- Crear una relación tarea-concepto -----------------
def create_tarea_concepto(db: Session, tarea_concepto_in: TareaConceptoCreate) -> TareaConcepto:
    """
    Crea una nueva relación entre una tarea y un concepto.
    """
    db_tarea_concepto = TareaConcepto(
        tarea_id=tarea_concepto_in.tarea_id,
        concepto_id=tarea_concepto_in.concepto_id,
        peso=Decimal(str(tarea_concepto_in.peso)) if tarea_concepto_in.peso else Decimal('1.0')
    )
    db.add(db_tarea_concepto)
    db.commit()
    db.refresh(db_tarea_concepto)
    return db_tarea_concepto

# ----------------- Asociar múltiples conceptos a una tarea -----------------
def associate_conceptos_to_tarea(db: Session, tarea_id: int, concepto_ids: List[int], pesos: Optional[List[float]] = None) -> List[TareaConcepto]:
    """
    Asocia múltiples conceptos a una tarea.
    Si se proporcionan pesos, se usan; de lo contrario, se usa 1.0 para todos.
    """
    # Eliminar relaciones existentes para esta tarea
    db.query(TareaConcepto).filter(TareaConcepto.tarea_id == tarea_id).delete()
    
    # Crear nuevas relaciones
    relaciones = []
    for idx, concepto_id in enumerate(concepto_ids):
        peso = Decimal(str(pesos[idx])) if pesos and idx < len(pesos) else Decimal('1.0')
        db_tarea_concepto = TareaConcepto(
            tarea_id=tarea_id,
            concepto_id=concepto_id,
            peso=peso
        )
        db.add(db_tarea_concepto)
        relaciones.append(db_tarea_concepto)
    
    db.commit()
    for rel in relaciones:
        db.refresh(rel)
    return relaciones

# ----------------- Obtener conceptos de una tarea -----------------
def get_conceptos_by_tarea(db: Session, tarea_id: int) -> List[TareaConcepto]:
    """
    Obtiene todos los conceptos asociados a una tarea.
    """
    return db.query(TareaConcepto).filter(TareaConcepto.tarea_id == tarea_id).all()

# ----------------- Obtener tareas de un concepto -----------------
def get_tareas_by_concepto(db: Session, concepto_id: int) -> List[TareaConcepto]:
    """
    Obtiene todas las tareas asociadas a un concepto.
    """
    return db.query(TareaConcepto).filter(TareaConcepto.concepto_id == concepto_id).all()

# ----------------- Eliminar una relación tarea-concepto -----------------
def delete_tarea_concepto(db: Session, tarea_id: int, concepto_id: int) -> bool:
    """
    Elimina una relación específica entre una tarea y un concepto.
    """
    db_tarea_concepto = db.query(TareaConcepto).filter(
        TareaConcepto.tarea_id == tarea_id,
        TareaConcepto.concepto_id == concepto_id
    ).first()
    if db_tarea_concepto:
        db.delete(db_tarea_concepto)
        db.commit()
        return True
    return False

# ----------------- Eliminar todas las relaciones de una tarea -----------------
def delete_all_tarea_conceptos(db: Session, tarea_id: int) -> int:
    """
    Elimina todas las relaciones de conceptos de una tarea.
    Retorna el número de relaciones eliminadas.
    """
    count = db.query(TareaConcepto).filter(TareaConcepto.tarea_id == tarea_id).delete()
    db.commit()
    return count




