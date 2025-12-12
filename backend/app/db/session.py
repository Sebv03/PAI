# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # Importa la configuración

# ¡Esta es la línea clave! Usa la URL que definimos en config.py
# Configuración mejorada del pool para evitar bloqueos
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_size=5,  # Número de conexiones a mantener en el pool
    max_overflow=10,  # Conexiones adicionales permitidas
    pool_timeout=30,  # Tiempo máximo de espera para obtener conexión (segundos)
    pool_recycle=3600  # Recicla conexiones después de 1 hora
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para los endpoints (la usa deps.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()