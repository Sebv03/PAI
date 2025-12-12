# backend/app/schemas/concepto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema base para Concepto
class ConceptoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    nivel: Optional[str] = None

# Esquema para crear un concepto
class ConceptoCreate(ConceptoBase):
    pass

# Esquema para actualizar un concepto
class ConceptoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    nivel: Optional[str] = None

# Esquema para representar un concepto completo
class Concepto(ConceptoBase):
    id: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)




