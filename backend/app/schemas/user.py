# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.user import UserRole # Importa el Enum

class UserBase(BaseModel):
    correo: EmailStr
    nombre_completo: Optional[str] = None

class UserCreate(UserBase):
    password: str
    rol: UserRole = UserRole.ESTUDIANTE # Permite especificar el rol al crear

class UserUpdate(BaseModel):
    password: Optional[str] = None
    nombre_completo: Optional[str] = None
    activo: Optional[bool] = None

class User(UserBase):
    id: int
    activo: bool
    rol: UserRole # <-- Retorna el rol
    
    model_config = ConfigDict(from_attributes=True) # para Pydantic v2