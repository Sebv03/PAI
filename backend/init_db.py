#!/usr/bin/env python
"""
Script para inicializar la base de datos en producción.
Ejecuta este script después de desplegar en Railway para crear las tablas.
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from app.db.base import Base

def init_database():
    """Crea todas las tablas en la base de datos."""
    try:
        print("🔄 Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        print("✅ ¡Tablas creadas exitosamente!")
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

