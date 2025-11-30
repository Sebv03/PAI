# 🚀 Guía Rápida - Configuración Local (PostgreSQL Local)

Este documento contiene las instrucciones para hacer funcionar el proyecto PAI Platform en tu entorno local **sin Docker**, usando PostgreSQL instalado localmente.

## ✅ Configuración Completada

Las siguientes configuraciones ya han sido ajustadas para tu entorno local:

- ✅ Credenciales de base de datos: `postgres/123` (PostgreSQL local, puerto 5433)
- ✅ Dependencias del backend instaladas
- ✅ Dependencias del ML service instaladas
- ✅ Dependencias del frontend instaladas
- ✅ Directorios necesarios creados

## 🎯 Inicio Rápido

### Opción 1: Usar el Script Automático (Recomendado)

```bash
./start_local.sh
```

Este script:
- Verifica que PostgreSQL esté instalado y corriendo
- Verifica si la base de datos existe
- Te muestra las instrucciones para iniciar los demás servicios

### Opción 2: Inicio Manual

#### 1. Verificar que PostgreSQL Esté Corriendo

```bash
pg_isready -h localhost -p 5433
```

Si no está corriendo, en macOS puedes iniciarlo con:
```bash
brew services start postgresql@14
# o
brew services start postgresql
```

#### 2. Crear la Base de Datos (Solo Primera Vez)

**Opción A - Usando el script:**
```bash
./create_database.sh postgres
# o con tu usuario:
./create_database.sh sebahenriquez
```

**Opción B - Manualmente:**
```bash
# Si tu usuario PostgreSQL es 'postgres' con contraseña '123':
PGPASSWORD=123 psql -U postgres -h localhost -p 5433 -c "CREATE DATABASE pai_db;"

# O si tu usuario tiene permisos sin contraseña:
createdb -p 5433 pai_db
```

**Opción C - Conectando directamente a psql:**
```bash
psql -U postgres -h localhost -p 5433
# Ingresa la contraseña cuando se solicite (123)
CREATE DATABASE pai_db;
\q
```

#### 3. Iniciar Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Verás: `Uvicorn running on http://0.0.0.0:8000`

#### 4. Iniciar ML Service (Terminal 2)

```bash
cd ml-service
source venv/bin/activate
python main.py
```

Verás: `Uvicorn running on http://0.0.0.0:8001`

#### 5. Iniciar Frontend (Terminal 3)

```bash
cd frontend
npm run dev
```

Verás: `Local: http://localhost:5173/`

## 🌐 URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **ML Service**: http://localhost:8001
- **ML Service Docs**: http://localhost:8001/docs

## 📋 Configuración Inicial (Primera Vez)

### Crear Usuario Administrador

Después de iniciar el backend, en una nueva terminal:

```bash
cd backend
source venv/bin/activate
python create_admin.py
```

Esto te pedirá crear un usuario administrador para acceder a la plataforma.

## 🛑 Detener Servicios

### Detener Backend/ML Service/Frontend
Presiona `Ctrl + C` en cada terminal

### Detener PostgreSQL (Opcional)
Si quieres detener PostgreSQL completamente:
```bash
# En macOS:
brew services stop postgresql@14
# o
brew services stop postgresql
```

## 🐛 Solución de Problemas

### Error: PostgreSQL no está corriendo

**En macOS:**
```bash
# Iniciar PostgreSQL
brew services start postgresql@14
# o
brew services start postgresql

# Verificar que está corriendo
pg_isready -h localhost -p 5433
```

**En Linux:**
```bash
sudo systemctl start postgresql
# o
sudo service postgresql start
```

### Error: No se puede conectar a la base de datos

1. **Verifica que PostgreSQL esté corriendo:**
   ```bash
   pg_isready -h localhost -p 5433
   ```

2. **Verifica que la base de datos exista:**
   ```bash
   PGPASSWORD=123 psql -U postgres -h localhost -p 5433 -l | grep pai_db
   ```

3. **Si la base de datos no existe, créala:**
   ```bash
   PGPASSWORD=123 psql -U postgres -h localhost -p 5433 -c "CREATE DATABASE pai_db;"
   ```

4. **Verifica las credenciales en:**
   - `backend/app/core/config.py` (línea 14)
   - `ml-service/core/config.py` (línea 14)
   
   Deben ser: `postgresql://postgres:123@localhost:5433/pai_db`

5. **Si usas un usuario diferente:**
   - Actualiza `DATABASE_URL` en ambos archivos de configuración
   - Asegúrate de que el usuario tenga permisos para crear bases de datos

### Error: "password authentication failed"

Si la contraseña no es `123` o el usuario no es `postgres`:

1. Verifica tu usuario y contraseña de PostgreSQL
2. Actualiza `DATABASE_URL` en:
   - `backend/app/core/config.py`
   - `ml-service/core/config.py`
   
   Formato: `postgresql://[usuario]:[contraseña]@localhost:5433/pai_db`

### Error: Puerto ya en uso

Si algún puerto está ocupado, puedes cambiarlo:

**Backend**: Modifica el puerto en el comando uvicorn:
```bash
uvicorn app.main:app --reload --port 8002
```

**ML Service**: Edita `ml-service/main.py` línea 292 y cambia el puerto

**Frontend**: Edita `frontend/vite.config.js` y agrega:
```js
export default defineConfig({
  server: {
    port: 5174
  }
})
```

### Error: Módulos no encontrados

Si falta alguna dependencia:

**Backend**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**ML Service**:
```bash
cd ml-service
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

## 📝 Credenciales de Base de Datos

- **Usuario**: `postgres`
- **Contraseña**: `123`
- **Base de datos**: `pai_db`
- **Puerto**: `5433`
- **Host**: `localhost`

Si usas credenciales diferentes, actualiza:
- `backend/app/core/config.py`
- `ml-service/core/config.py`

## 💡 Tips

- Mantén las 3 terminales abiertas mientras trabajas (Backend, ML Service, Frontend)
- El backend y ML service tienen `--reload` para recargar automáticamente
- El frontend de Vite también recarga automáticamente
- Los cambios en el código se reflejan inmediatamente
- PostgreSQL debe estar corriendo antes de iniciar el backend o ML service

## 🔧 Verificar Conexión a la Base de Datos

Para probar que puedes conectarte:
```bash
PGPASSWORD=123 psql -U postgres -h localhost -p 5433 -d pai_db -c "SELECT version();"
```

## 📚 Más Información

Para más detalles, consulta `INICIO_LOCAL.md`

---

**¡Listo! 🎉 Ya puedes empezar a desarrollar.**
