# backend/app/crud/crud_concepto.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.concepto import Concepto
from app.schemas.concepto import ConceptoCreate, ConceptoUpdate

# ----------------- Crear un nuevo concepto -----------------
def create_concepto(db: Session, concepto_in: ConceptoCreate) -> Concepto:
    """
    Crea un nuevo concepto en la base de datos.
    """
    db_concepto = Concepto(
        nombre=concepto_in.nombre,
        descripcion=concepto_in.descripcion,
        categoria=concepto_in.categoria,
        nivel=concepto_in.nivel
    )
    db.add(db_concepto)
    db.commit()
    db.refresh(db_concepto)
    return db_concepto

# ----------------- Obtener un concepto por ID -----------------
def get_concepto_by_id(db: Session, concepto_id: int) -> Optional[Concepto]:
    """
    Obtiene un concepto específico por su ID.
    """
    return db.query(Concepto).filter(Concepto.id == concepto_id).first()

# ----------------- Obtener un concepto por nombre -----------------
def get_concepto_by_nombre(db: Session, nombre: str) -> Optional[Concepto]:
    """
    Obtiene un concepto por su nombre.
    """
    return db.query(Concepto).filter(Concepto.nombre == nombre).first()

# ----------------- Obtener todos los conceptos -----------------
def get_conceptos(db: Session, skip: int = 0, limit: int = 100) -> List[Concepto]:
    """
    Obtiene todos los conceptos existentes en la base de datos.
    """
    return db.query(Concepto).offset(skip).limit(limit).all()

# ----------------- Obtener conceptos por categoría -----------------
def get_conceptos_by_categoria(db: Session, categoria: str, skip: int = 0, limit: int = 100) -> List[Concepto]:
    """
    Obtiene todos los conceptos de una categoría específica.
    """
    return db.query(Concepto).filter(Concepto.categoria == categoria).offset(skip).limit(limit).all()

# ----------------- Obtener conceptos por nivel -----------------
def get_conceptos_by_nivel(db: Session, nivel: str, skip: int = 0, limit: int = 100) -> List[Concepto]:
    """
    Obtiene todos los conceptos de un nivel específico.
    """
    return db.query(Concepto).filter(Concepto.nivel == nivel).offset(skip).limit(limit).all()

# ----------------- Actualizar un concepto -----------------
def update_concepto(db: Session, db_concepto: Concepto, concepto_in: ConceptoUpdate) -> Concepto:
    """
    Actualiza un concepto existente en la base de datos.
    """
    update_data = concepto_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_concepto, field, value)
    
    db.add(db_concepto)
    db.commit()
    db.refresh(db_concepto)
    return db_concepto

# ----------------- Eliminar un concepto -----------------
def delete_concepto(db: Session, concepto_id: int) -> Optional[Concepto]:
    """
    Elimina un concepto específico por su ID.
    """
    db_concepto = db.query(Concepto).filter(Concepto.id == concepto_id).first()
    if db_concepto:
        db.delete(db_concepto)
        db.commit()
    return db_concepto

# ----------------- Obtener categorías de conceptos usados en los cursos de un profesor -----------------
def get_categorias_conceptos_by_teacher_courses(db: Session, teacher_id: int) -> List[str]:
    """
    Obtiene las categorías únicas de conceptos que están asociados a tareas
    de los cursos que pertenecen a un profesor específico.
    
    Retorna una lista de nombres de categorías (sin duplicados).
    """
    from app.models.course import Course
    from app.models.task import Task
    from app.models.tarea_concepto import TareaConcepto
    
    # Query: Obtener categorías únicas de conceptos usados en tareas de cursos del profesor
    categorias = db.query(Concepto.categoria).distinct().join(
        TareaConcepto, TareaConcepto.concepto_id == Concepto.id
    ).join(
        Task, Task.id == TareaConcepto.tarea_id
    ).join(
        Course, Course.id == Task.curso_id
    ).filter(
        Course.propietario_id == teacher_id,
        Concepto.categoria.isnot(None),
        Concepto.categoria != ''
    ).all()
    
    # Extraer solo los valores de las tuplas y filtrar None
    return [cat[0] for cat in categorias if cat[0] is not None and cat[0].strip() != '']

# ----------------- Obtener conceptos por categorías -----------------
def get_conceptos_by_categorias(db: Session, categorias: List[str], skip: int = 0, limit: int = 100) -> List[Concepto]:
    """
    Obtiene todos los conceptos que pertenecen a alguna de las categorías especificadas.
    """
    if not categorias:
        return []
    
    return db.query(Concepto).filter(
        Concepto.categoria.in_(categorias)
    ).offset(skip).limit(limit).all()


