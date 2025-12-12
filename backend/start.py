#!/usr/bin/env python
"""
Script de inicio para Railway.
Lee el puerto desde la variable de entorno PORT que Railway proporciona automáticamente.
"""
import os
import sys

# Obtener el puerto desde la variable de entorno PORT (Railway lo proporciona)
port = int(os.environ.get("PORT", 8000))

# Ejecutar uvicorn con el puerto correcto
if __name__ == "__main__":
    os.execvp(
        "uvicorn",
        [
            "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ]
    )

