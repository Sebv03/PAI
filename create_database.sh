#!/bin/bash

# Script para crear la base de datos pai_db en PostgreSQL local

echo "📦 Creando base de datos pai_db..."
echo ""

# Solicitar usuario de PostgreSQL
if [ -z "$1" ]; then
    echo "Uso: ./create_database.sh [usuario_postgres]"
    echo ""
    echo "Ejemplo:"
    echo "  ./create_database.sh postgres"
    echo "  ./create_database.sh sebahenriquez"
    echo ""
    echo "Nota: Se usará la contraseña 123 y el puerto 5433"
    exit 1
fi

PG_USER=$1

echo "Intentando crear base de datos con usuario: $PG_USER"
echo ""

# Verificar si la base de datos ya existe
PGPASSWORD=123 psql -U $PG_USER -h localhost -p 5433 -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw pai_db
if [ $? -eq 0 ]; then
    echo "✅ La base de datos 'pai_db' ya existe"
    exit 0
fi

# Intentar crear la base de datos
PGPASSWORD=123 psql -U $PG_USER -h localhost -p 5433 -c "CREATE DATABASE pai_db;" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Base de datos 'pai_db' creada exitosamente"
else
    echo ""
    echo "❌ Error al crear la base de datos"
    echo ""
    echo "Por favor, crea la base de datos manualmente con uno de estos comandos:"
    echo ""
    echo "  # Si el usuario es 'postgres':"
    echo "  PGPASSWORD=123 psql -U postgres -h localhost -p 5433 -c 'CREATE DATABASE pai_db;'"
    echo ""
    echo "  # Si el usuario es tu usuario del sistema:"
    echo "  createdb pai_db"
    echo ""
    echo "  # O conecta a PostgreSQL y ejecuta:"
    echo "  psql -U [tu_usuario]"
    echo "  CREATE DATABASE pai_db;"
    exit 1
fi

