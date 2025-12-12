# backend/app/schemas/tarea_concepto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

# Esquema base para TareaConcepto
class TareaConceptoBase(BaseModel):
    tarea_id: int
    concepto_id: int
    peso: Optional[Decimal] = 1.0

# Esquema para crear una relación tarea-concepto
class TareaConceptoCreate(TareaConceptoBase):
    pass

# Esquema para actualizar una relación tarea-concepto
class TareaConceptoUpdate(BaseModel):
    peso: Optional[Decimal] = None

# Esquema para representar una relación tarea-concepto completa
class TareaConcepto(TareaConceptoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Esquema para asociar múltiples conceptos a una tarea
class TareaConceptosCreate(BaseModel):
    concepto_ids: list[int]  # Lista de IDs de conceptos
    pesos: Optional[list[float]] = None  # Pesos opcionales para cada concepto




