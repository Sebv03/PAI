# backend/app/core/config.py
from pydantic_settings import BaseSettings # Asegúrate de usar pydantic_settings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plataforma Académica Inteligente PAI"
    API_V1_STR: str = "/api/v1"
    
    # CORS - Permitir múltiples orígenes (separados por comas)
    # En producción, usa variables de entorno como string separado por comas
    # Ejemplo: "https://app.vercel.app,https://app2.vercel.app"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    
    def get_cors_origins(self) -> List[str]:
        """Retorna BACKEND_CORS_ORIGINS como lista de strings"""
        if not self.BACKEND_CORS_ORIGINS:
            return ["http://localhost:5173", "http://127.0.0.1:5173"]
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
    
    # --- ¡CRÍTICO! Tu URL de Base de Datos para PostgreSQL ---
    # En producción, usarás la variable de entorno DATABASE_URL de Railway/Render/Supabase
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:123@localhost:5433/pai_db"
    )
    
    # --- ¡CRÍTICO! Claves de Seguridad ---
    # IMPORTANTE: Genera una nueva para producción
    # Python: import secrets; print(secrets.token_hex(32))
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = "HS256" # Deja este valor, es estándar
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # --- Directorio para almacenar archivos subidos ---
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads/submissions")
    
    # URL del Servicio ML (para producción)


    class Config:
        case_sensitive = True

settings = Settings()