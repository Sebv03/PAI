#!/bin/bash
# Script de inicio para Railway
# Lee el puerto desde la variable de entorno PORT (Railway lo proporciona automáticamente)

# Si PORT no está definido, usa 8000 por defecto
PORT=${PORT:-8000}

# Ejecutar uvicorn con el puerto correcto
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT

