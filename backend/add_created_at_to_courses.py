# Script para agregar la columna created_at a la tabla courses
# Ejecuta este script una vez para actualizar la base de datos

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_created_at_column():
    """Agrega la columna created_at a la tabla courses si no existe"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar si la columna ya existe
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='courses' AND column_name='created_at'
        """)
        result = conn.execute(check_query)
        
        if result.fetchone():
            print("✅ La columna 'created_at' ya existe en la tabla 'courses'.")
        else:
            # Agregar la columna con valor por defecto NOW()
            alter_query = text("""
                ALTER TABLE courses 
                ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Columna 'created_at' agregada exitosamente a la tabla 'courses'.")
    
    print("✅ Migración completada.")

if __name__ == "__main__":
    add_created_at_column()


