# backend/app/schemas/recurso_concepto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

# Esquema base para RecursoConcepto
class RecursoConceptoBase(BaseModel):
    recurso_id: int
    concepto_id: int
    relevancia: Optional[Decimal] = 1.0

# Esquema para crear una relación recurso-concepto
class RecursoConceptoCreate(RecursoConceptoBase):
    pass

# Esquema para actualizar una relación recurso-concepto
class RecursoConceptoUpdate(BaseModel):
    relevancia: Optional[Decimal] = None

# Esquema para representar una relación recurso-concepto completa
class RecursoConcepto(RecursoConceptoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Esquema para asociar múltiples conceptos a un recurso
class RecursoConceptosCreate(BaseModel):
    concepto_ids: list[int]  # Lista de IDs de conceptos
    relevancias: Optional[list[float]] = None  # Relevancias opcionales para cada concepto




