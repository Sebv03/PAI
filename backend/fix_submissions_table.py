# Script para corregir la tabla submissions
# Cambia user_id a student_id

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_submissions_table():
    """Corrige la tabla submissions"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar columnas actuales
        check_columns = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='submissions'
            ORDER BY ordinal_position
        """)
        result = conn.execute(check_columns)
        columns = [row[0] for row in result.fetchall()]
        
        print(f"Columnas actuales en submissions: {columns}")
        
        # Si existe user_id y no existe student_id, cambiar user_id a student_id
        if 'user_id' in columns and 'student_id' not in columns:
            print("Cambiando user_id a student_id...")
            rename_query = text("""
                ALTER TABLE submissions 
                RENAME COLUMN user_id TO student_id
            """)
            conn.execute(rename_query)
            conn.commit()
            print("✅ Columna user_id renombrada a student_id")
        
        # Asegurar que submitted_at tenga timezone
        if 'submitted_at' in columns:
            check_tz = text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name='submissions' AND column_name='submitted_at'
            """)
            result = conn.execute(check_tz)
            data_type = result.fetchone()[0]
            
            if 'time' in data_type and 'time zone' not in data_type:
                print("Actualizando submitted_at para incluir timezone...")
                alter_tz = text("""
                    ALTER TABLE submissions 
                    ALTER COLUMN submitted_at TYPE TIMESTAMP WITH TIME ZONE 
                    USING submitted_at AT TIME ZONE 'UTC'
                """)
                conn.execute(alter_tz)
                conn.commit()
                print("✅ Columna submitted_at actualizada con timezone")
    
    print("✅ Migración completada.")

if __name__ == "__main__":
    fix_submissions_table()


