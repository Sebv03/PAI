#!/bin/bash

# Script de inicio rápido para PAI Platform (entorno local SIN Docker)
# Este script verifica PostgreSQL y proporciona instrucciones para iniciar los servicios

echo "🚀 Iniciando PAI Platform - Entorno Local (PostgreSQL Local)"
echo "=============================================================="
echo ""

# Verificar que PostgreSQL esté instalado
if ! command -v psql &> /dev/null; then
    echo "❌ Error: PostgreSQL no está instalado"
    echo "   Por favor, instala PostgreSQL desde https://www.postgresql.org/download/"
    exit 1
fi

echo "✅ PostgreSQL está instalado"
echo ""

# Verificar que PostgreSQL esté corriendo
if ! pg_isready -h localhost -p 5433 &> /dev/null; then
    echo "❌ Error: PostgreSQL no está corriendo en el puerto 5433"
    echo ""
    echo "   Verifica que PostgreSQL esté configurado en el puerto 5433"
    echo "   En macOS, inicia PostgreSQL con:"
    echo "     brew services start postgresql@14"
    echo "   o"
    echo "     brew services start postgresql"
    echo ""
    exit 1
fi

echo "✅ PostgreSQL está corriendo en el puerto 5433"
echo ""

# Verificar si la base de datos existe
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_EXISTS=false

# Intentar diferentes usuarios comunes
for PG_USER in postgres sebahenriquez $USER; do
    if PGPASSWORD=123 psql -U $PG_USER -h localhost -p 5433 -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw pai_db; then
        echo "✅ La base de datos 'pai_db' ya existe"
        DB_EXISTS=true
        break
    fi
done

if [ "$DB_EXISTS" = false ]; then
    echo "⚠️  La base de datos 'pai_db' no existe"
    echo ""
    echo "📦 Para crear la base de datos, ejecuta uno de estos comandos:"
    echo ""
    echo "   Opción 1 - Si conoces tu usuario de PostgreSQL:"
    echo "     ./create_database.sh [tu_usuario]"
    echo ""
    echo "   Opción 2 - Crear manualmente con psql:"
    echo "     PGPASSWORD=123456 psql -U postgres -h localhost -p 5432 -c 'CREATE DATABASE pai_db;'"
    echo ""
    echo "   Opción 3 - Si tu usuario tiene permisos sin contraseña:"
    echo "     createdb pai_db"
    echo ""
    echo "   Nota: Las credenciales configuradas son usuario 'postgres', contraseña '123', puerto '5433'"
    echo "         Si usas otro usuario, actualiza las configuraciones en:"
    echo "         - backend/app/core/config.py"
    echo "         - ml-service/core/config.py"
    echo ""
fi

echo ""
echo "=============================================================="
echo "✅ Verificación completada"
echo ""
echo "📋 Para iniciar los servicios, abre 3 terminales:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd $PROJECT_DIR/backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 - ML Service:"
echo "  cd $PROJECT_DIR/ml-service"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 3 - Frontend:"
echo "  cd $PROJECT_DIR/frontend"
echo "  npm run dev"
echo ""
echo "🌐 URLs importantes:"
echo "  - Frontend: http://localhost:5173"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - ML Service: http://localhost:8001"
echo ""
echo "💡 Primera vez:"
echo "  Después de iniciar el backend, crea un administrador:"
echo "  cd $PROJECT_DIR/backend"
echo "  source venv/bin/activate"
echo "  python create_admin.py"
echo ""
