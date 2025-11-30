#!/usr/bin/env python3
"""
Script para corregir las secuencias de IDs en todas las tablas
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_sequences():
    """Corrige las secuencias de IDs en todas las tablas"""
    engine = create_engine(settings.DATABASE_URL)
    
    # Lista de tablas con secuencias
    tables = [
        'users',
        'courses',
        'tasks',
        'enrollments',
        'submissions',
        'announcements',
        'comments',
        'student_profiles'
    ]
    
    with engine.connect() as conn:
        for table in tables:
            try:
                # Obtener el máximo ID actual
                max_id_result = conn.execute(text(f'SELECT MAX(id) FROM {table}'))
                max_id = max_id_result.fetchone()[0]
                
                if max_id is None:
                    max_id = 0
                    print(f"Tabla {table}: vacía, secuencia se establecerá en 1")
                else:
                    print(f"Tabla {table}: max_id = {max_id}")
                
                # Obtener el valor actual de la secuencia
                try:
                    seq_result = conn.execute(text(f"SELECT last_value FROM {table}_id_seq"))
                    seq_value = seq_result.fetchone()[0]
                    print(f"  Secuencia actual: {seq_value}")
                except Exception as e:
                    print(f"  ⚠️  No se pudo leer la secuencia: {e}")
                    continue
                
                # Resetear la secuencia si es necesario
                if seq_value <= max_id:
                    new_value = max_id + 1
                    conn.execute(text(f"SELECT setval('{table}_id_seq', {new_value}, false)"))
                    conn.commit()
                    print(f"  ✅ Secuencia reseteada a {new_value}")
                else:
                    print(f"  ✅ Secuencia está correcta")
                    
            except Exception as e:
                print(f"  ❌ Error procesando {table}: {e}")
        
        print("\n✅ Proceso completado.")

if __name__ == "__main__":
    fix_sequences()

