#!/bin/bash

# Script para iniciar el backend asegurándose de usar el entorno virtual

cd "$(dirname "$0")"

# Activar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encuentra el entorno virtual. Por favor, créalo primero:"
    echo "   python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

# Verificar que python-jose esté instalado
if ! python -c "from jose import jwt" 2>/dev/null; then
    echo "❌ Error: python-jose no está instalado. Instalando..."
    pip install 'python-jose[cryptography]==3.3.0'
fi

# Verificar que todas las dependencias estén instaladas
if [ -f "requirements.txt" ]; then
    echo "📦 Verificando dependencias..."
    pip install -q -r requirements.txt
fi

# Iniciar el servidor
echo "🚀 Iniciando backend en http://localhost:8000"
echo "📚 Documentación disponible en http://localhost:8000/docs"
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

