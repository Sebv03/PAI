# backend/create_recommendation_tables.py
"""
Script Python para crear las tablas del Sistema de Recomendación de Contenido Remedial.
Este script lee el archivo SQL y lo ejecuta en la base de datos.
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
from pathlib import Path

def create_recommendation_tables():
    """
    Crea todas las tablas necesarias para el sistema de recomendaciones.
    """
    # Leer el archivo SQL
    sql_file = Path(__file__).parent / "create_recommendation_tables.sql"
    
    if not sql_file.exists():
        print(f"❌ Error: No se encontró el archivo {sql_file}")
        return False
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Ejecutar el script SQL
            # Dividir por ';' y ejecutar cada statement
            statements = [s.strip() + ';' for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
            
            for statement in statements:
                if statement.strip() and statement.strip() != ';':
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        # Ignorar errores de "ya existe" para tablas e índices
                        if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                            print(f"⚠️  Advertencia al ejecutar statement: {e}")
            
            print("✅ Tablas del sistema de recomendaciones creadas exitosamente")
            print("   - conceptos")
            print("   - recursos")
            print("   - tarea_conceptos")
            print("   - recurso_conceptos")
            print("   - recomendaciones_estudiantes")
            print("   - interacciones_recursos")
            return True
            
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_recommendation_tables()




