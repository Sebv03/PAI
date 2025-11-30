# Script para corregir la tabla enrollments
# Cambia user_id a student_id y agrega enrollment_date si falta

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_enrollments_table():
    """Corrige la tabla enrollments"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar columnas actuales
        check_columns = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='enrollments'
            ORDER BY ordinal_position
        """)
        result = conn.execute(check_columns)
        columns = [row[0] for row in result.fetchall()]
        
        print(f"Columnas actuales en enrollments: {columns}")
        
        # Si existe user_id y no existe student_id, cambiar user_id a student_id
        if 'user_id' in columns and 'student_id' not in columns:
            print("Cambiando user_id a student_id...")
            rename_query = text("""
                ALTER TABLE enrollments 
                RENAME COLUMN user_id TO student_id
            """)
            conn.execute(rename_query)
            conn.commit()
            print("✅ Columna user_id renombrada a student_id")
        
        # Verificar si enrollment_date existe
        if 'enrollment_date' not in columns:
            print("Agregando columna enrollment_date...")
            alter_query = text("""
                ALTER TABLE enrollments 
                ADD COLUMN enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Columna enrollment_date agregada")
        else:
            print("✅ La columna enrollment_date ya existe")
    
    print("✅ Migración completada.")

if __name__ == "__main__":
    fix_enrollments_table()


