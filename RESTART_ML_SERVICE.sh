#!/bin/bash

# Script para reiniciar el servicio ML

echo "🔄 Reiniciando servicio ML..."

# Detener proceso existente si está corriendo
if lsof -ti:8001 > /dev/null 2>&1; then
    echo "Deteniendo servicio ML existente..."
    kill $(lsof -ti:8001)
    sleep 2
fi

echo "Iniciando servicio ML..."
cd "$(dirname "$0")/ml-service"
source venv/bin/activate
python main.py


