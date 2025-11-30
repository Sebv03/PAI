# backend/fix_submissions_fecha_entrega.py
"""
Script para corregir submissions que tienen fecha_entrega como None.
Establece una fecha por defecto basada en la fecha de creación o la fecha actual.
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
from datetime import datetime, timezone

def fix_submissions_fecha_entrega():
    """
    Actualiza todas las submissions que tienen fecha_entrega como None.
    """
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # Buscar submissions con fecha_entrega NULL
        check_query = text("""
            SELECT id, fecha_entrega
            FROM submissions
            WHERE fecha_entrega IS NULL
        """)
        result = conn.execute(check_query)
        submissions_without_date = result.fetchall()
        
        if not submissions_without_date:
            print("✅ No hay submissions con fecha_entrega NULL.")
            return
        
        print(f"⚠️ Encontradas {len(submissions_without_date)} submissions sin fecha_entrega.")
        
        # Actualizar cada submission con la fecha actual
        current_date = datetime.now(timezone.utc)
        update_query = text("""
            UPDATE submissions
            SET fecha_entrega = :fecha
            WHERE fecha_entrega IS NULL
        """)
        
        conn.execute(update_query, {"fecha": current_date})
        conn.commit()
        
        print(f"✅ Actualizadas {len(submissions_without_date)} submissions con fecha: {current_date}")

if __name__ == "__main__":
    fix_submissions_fecha_entrega()

