#!/usr/bin/env python3
"""
Script para hacer nullable las columnas contenido y ruta_archivo en la tabla submissions
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_submissions_nullable():
    """Hace nullable las columnas contenido y ruta_archivo en submissions"""
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # Verificar estado actual
        check_query = text("""
            SELECT column_name, is_nullable
            FROM information_schema.columns
            WHERE table_name='submissions' 
            AND column_name IN ('contenido', 'ruta_archivo')
        """)
        result = conn.execute(check_query)
        current_state = {row[0]: row[1] for row in result.fetchall()}
        
        print("Estado actual de las columnas:")
        for col, nullable in current_state.items():
            print(f"  {col}: nullable={nullable}")
        
        # Hacer contenido nullable
        if 'contenido' in current_state and current_state['contenido'] == 'NO':
            print("\nHaciendo 'contenido' nullable...")
            alter_query = text("""
                ALTER TABLE submissions 
                ALTER COLUMN contenido DROP NOT NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Columna 'contenido' ahora es nullable")
        else:
            print("✅ Columna 'contenido' ya es nullable")
        
        # Hacer ruta_archivo nullable (por si acaso)
        if 'ruta_archivo' in current_state and current_state['ruta_archivo'] == 'NO':
            print("\nHaciendo 'ruta_archivo' nullable...")
            alter_query = text("""
                ALTER TABLE submissions 
                ALTER COLUMN ruta_archivo DROP NOT NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Columna 'ruta_archivo' ahora es nullable")
        else:
            print("✅ Columna 'ruta_archivo' ya es nullable")
        
        print("\n✅ Migración completada.")

if __name__ == "__main__":
    fix_submissions_nullable()

