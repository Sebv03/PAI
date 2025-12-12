# 🚀 Guía de Despliegue Gratuito en Internet

Esta guía te ayudará a desplegar tu plataforma PAI completamente en internet usando servicios gratuitos.

## 📋 Servicios que usaremos (100% GRATIS)

1. **Railway** - Backend API + Base de datos PostgreSQL (Tier gratuito: $5 créditos/mes)
2. **Vercel** - Frontend React (Tier gratuito ilimitado)

---

## 📝 PASO 1: Preparar el Código

### 1.1 Generar SECRET_KEY para producción

Ejecuta en tu terminal (Windows PowerShell):

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**Guarda esta clave**, la necesitarás en el Paso 3.

---

## 📝 PASO 2: Crear cuenta en Railway

1. Ve a https://railway.app
2. Haz clic en **"Login"** → **"Start a New Project"**
3. Inicia sesión con GitHub (recomendado) o Email
4. Autoriza Railway a acceder a tu repositorio

---
postgresql://postgres:olzGvwkrSAzQCQfbUOwuGLcwsoJWyLTR@postgres.railway.internal:5432/railway

## 📝 PASO 3: Desplegar Base de Datos PostgreSQL en Railway

1. En Railway, haz clic en **"New Project"**
2. Selecciona **"Empty Project"**
3. Haz clic en **"+ New"** → **"Database"** → **"Add PostgreSQL"**
4. Espera a que se cree (30-60 segundos)
5. Haz clic en la base de datos creada
6. Ve a la pestaña **"Variables"**
7. Copia el valor de **`DATABASE_URL`** (ejemplo: `postgresql://postgres:xxx@containers-us-west-xxx.railway.app:5432/railway`)
8. **¡GUARDA ESTA URL!** La necesitarás en el siguiente paso

---

## 📝 PASO 4: Desplegar Backend en Railway

### 4.1 Subir código del backend

1. En Railway, en el mismo proyecto, haz clic en **"+ New"** → **"GitHub Repo"**
2. Selecciona tu repositorio
3. Railway detectará automáticamente el backend

### 4.2 Configurar Backend en Railway

1. Haz clic en el servicio del backend (tarjeta "PAI")
2. Ve a la pestaña **"Settings"**
3. En la sección **"Source"**, configura:
   - **Root Directory**: `backend`
4. En la sección **"Build"**, configura:
   - **Build Command**: `pip install -r requirements.txt` (o déjalo en blanco, Railway lo detectará automáticamente)
5. En la sección **"Deploy"**, configura:
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4.3 Configurar Variables de Entorno

En la pestaña **"Variables"**, agrega estas variables:

```
DATABASE_URL=postgresql://postgres:xxx@containers-us-west-xxx.railway.app:5432/railway
SECRET_KEY=tu_clave_generada_en_paso_1
BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app
UPLOAD_DIR=uploads/submissions
```

**Importante:**
- Reemplaza `DATABASE_URL` con la URL que copiaste en el Paso 3
- Reemplaza `SECRET_KEY` con la clave que generaste en el Paso 1
- Por ahora deja `BACKEND_CORS_ORIGINS` con un valor temporal, lo actualizarás después

### 4.4 Desplegar el Backend

**IMPORTANTE:** Primero debes hacer el deploy antes de poder generar el dominio.

1. En Railway, haz clic en el botón **"Deploy"** (arriba a la izquierda, botón morado con flecha hacia arriba)
2. O presiona **Ctrl+Enter** (o **Cmd+Enter** en Mac)
3. Espera a que el build y deploy se complete (puede tomar 2-5 minutos)
4. Verás el progreso en la pestaña **"Deployments"**

### 4.5 Obtener URL del Backend (DESPUÉS del deploy)

**Solo después de que el deploy esté completo:**

1. Ve a la pestaña **"Settings"** del backend
2. En la sección **"Networking"** → **"Public Networking"**
3. Verás un campo que dice **"Public domain will be generated"**
4. Haz clic en el ícono de **globo** 🌐 o en el campo mismo
5. Railway generará automáticamente un dominio (ejemplo: `https://pai-production.up.railway.app`)
6. **¡GUARDA ESTA URL!** La necesitarás para el frontend

**Si no aparece el dominio:**
- Asegúrate de que el deploy haya terminado exitosamente (verifica en "Deployments")
- Verifica que no haya errores en los logs
- Intenta hacer clic en el botón **"Generate Domain"** si está visible
- Si aún no funciona, ve a **"Settings"** → **"Networking"** → activa **"Public Networking"**

### 4.6 Verificar que el Backend funciona

1. Ve a: `https://tu-backend-url.railway.app/docs`
2. Deberías ver la documentación de Swagger de FastAPI
3. Si no carga, revisa los logs en la pestaña **"Deployments"** o **"Metrics"**

---

## 📝 PASO 5: Crear cuenta en Vercel

1. Ve a https://vercel.com
2. Haz clic en **"Sign Up"**
3. Inicia sesión con GitHub (recomendado)

---

## 📝 PASO 6: Desplegar Frontend en Vercel

### 6.1 Importar Proyecto

1. En Vercel, haz clic en **"Add New"** → **"Project"**
2. Importa tu repositorio de GitHub
3. Selecciona el repositorio

### 6.2 Configurar Build

1. **Framework Preset**: Vite
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`

### 6.3 Variables de Entorno del Frontend

En la sección **"Environment Variables"**, agrega:

```
VITE_API_BASE_URL=https://tu-backend-url.railway.app
```

**Importante:** Reemplaza con la URL de tu backend de Railway del Paso 4.4

### 6.4 Desplegar

1. Haz clic en **"Deploy"**
2. Espera 2-3 minutos a que se complete el build
3. Vercel te dará una URL (ejemplo: `https://pai-platform.vercel.app`)
4. **¡GUARDA ESTA URL!**

---

## 📝 PASO 7: Actualizar CORS del Backend

1. Vuelve a Railway → Tu Backend → Variables
2. Actualiza `BACKEND_CORS_ORIGINS` con la URL de tu frontend:
   ```
   BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app
   ```
3. Railway reiniciará automáticamente el backend

---

## 📝 PASO 8: Configurar Base de Datos (Crear Tablas)

### Opción A: Usar Railway CLI (Recomendado)

1. Instala Railway CLI:
   ```powershell
   npm install -g @railway/cli
   ```

2. Inicia sesión:
   ```powershell
   railway login
   ```

3. Vincula tu proyecto:
   ```powershell
   railway link
   ```
   (Selecciona tu proyecto y servicio backend)

4. Ejecuta el script de inicialización:
   ```powershell
   railway run python
   ```
   Luego en Python:
   ```python
   from app.db.session import engine
   from app.db.base import Base
   Base.metadata.create_all(bind=engine)
   print("✅ Tablas creadas!")
   exit()
   ```

### Opción B: Crear Admin y Tablas desde tu máquina local

1. En tu máquina local, crea un archivo `.env` en la carpeta `backend/`:
   ```
   DATABASE_URL=postgresql://postgres:xxx@containers-us-west-xxx.railway.app:5432/railway
   SECRET_KEY=tu_secret_key
   ```

2. Ejecuta:
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python -c "from app.db.session import engine; from app.db.base import Base; Base.metadata.create_all(bind=engine); print('✅ Tablas creadas!')"
   ```

3. Crea el usuario administrador:
   ```powershell
   python create_admin.py
   ```
   (Ingresa email y contraseña cuando se te pida)

---

## 📝 PASO 9: Verificar que Todo Funciona

1. Abre tu frontend en Vercel: `https://tu-frontend.vercel.app`
2. Intenta hacer login con el usuario admin que creaste
3. Si todo funciona, ¡FELICIDADES! 🎉

---

## 🔧 Solución de Problemas

### Error: "CORS policy"
- Verifica que `BACKEND_CORS_ORIGINS` en Railway tenga exactamente la URL de tu frontend de Vercel

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` en Railway sea correcta
- Asegúrate de que la base de datos esté activa en Railway

### Error: "Cannot find module"
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa los logs en Railway → Deployments → Logs

### Frontend no carga
- Verifica que `VITE_API_BASE_URL` en Vercel sea correcta
- Revisa la consola del navegador (F12) para errores

### Archivos no se suben
- Los archivos se guardan en el filesystem de Railway (temporal)
- Para producción, considera usar AWS S3 o similar (requiere configuración adicional)

---

## 📊 Costos

**GRATIS si:**
- Railway: Usas menos de $5 en créditos/mes (suficiente para desarrollo/pequeña producción)
- Vercel: Tier gratuito ilimitado para proyectos personales

**Límites del tier gratuito:**
- Railway: $5 créditos/mes (~500 horas de ejecución)
- Vercel: Ilimitado para proyectos personales
- Base de datos: ~100MB gratis en Railway

---

## 🎯 URLs Finales

Al final tendrás:
- **Frontend**: `https://tu-frontend.vercel.app`
- **Backend API**: `https://tu-backend.railway.app`
- **Documentación API**: `https://tu-backend.railway.app/docs`
- **Base de datos**: Gestionada automáticamente por Railway

---

## 📝 Notas Importantes

1. **Archivos subidos**: Se guardan en el filesystem de Railway, que es temporal. Para producción, considera migrar a S3.

2. **Secret Key**: NUNCA compartas tu SECRET_KEY públicamente.

3. **Base de datos**: Railway puede pausar bases de datos inactivas en el tier gratuito. Reactívalas desde el dashboard.

4. **Dominio personalizado**: Puedes agregar tu propio dominio en Vercel y Railway (configuración adicional).

---

¡Listo! Tu plataforma está ahora en internet. 🚀

