# Script para agregar la columna enrollment_date a la tabla enrollments
# Ejecuta este script una vez para actualizar la base de datos

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_enrollment_date_column():
    """Agrega la columna enrollment_date a la tabla enrollments si no existe"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar si la columna ya existe
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='enrollments' AND column_name='enrollment_date'
        """)
        result = conn.execute(check_query)
        
        if result.fetchone():
            print("✅ La columna 'enrollment_date' ya existe en la tabla 'enrollments'.")
        else:
            # Agregar la columna con valor por defecto NOW()
            alter_query = text("""
                ALTER TABLE enrollments 
                ADD COLUMN enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Columna 'enrollment_date' agregada exitosamente a la tabla 'enrollments'.")
    
    print("✅ Migración completada.")

if __name__ == "__main__":
    add_enrollment_date_column()


