#!/bin/bash

# Script para iniciar el servicio ML

cd "$(dirname "$0")"

# Verificar que el entorno virtual exista
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encuentra el entorno virtual. Por favor, créalo primero:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar que las dependencias estén instaladas
if [ -f "requirements.txt" ]; then
    echo "📦 Verificando dependencias..."
    pip install -q -r requirements.txt
fi

# Iniciar el servidor
echo "🤖 Iniciando servicio ML en http://localhost:8001"
echo "📚 Documentación disponible en http://localhost:8001/docs"
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""
uvicorn main:app --reload --port 8001 --host 0.0.0.0

