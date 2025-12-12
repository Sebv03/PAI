# 🔧 Solución: Railway cambia automáticamente el Start Command

## ❌ Problema
Railway está cambiando automáticamente el **Start Command** a `bash start.sh` incluso después de que lo cambias manualmente.

## 🔍 Causa
Railway lee el archivo `railway.json` (o `backend/railway.json`) y usa la configuración de `startCommand` que está ahí. Si el archivo tiene `bash start.sh`, Railway lo aplicará automáticamente.

## ✅ Solución

### Opción 1: Actualizar railway.json (Recomendado)

He actualizado los archivos `railway.json` para usar el comando de Python directamente:

1. **Haz pull de los cambios** en Railway (o espera a que Railway detecte los cambios automáticamente)
2. Railway debería detectar el cambio y actualizar el Start Command automáticamente
3. Si no se actualiza automáticamente, ve a **Settings** → **Deploy** y verifica que el comando sea:
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

### Opción 2: Eliminar railway.json temporalmente

Si Railway sigue usando el archivo antiguo:

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia manualmente el **Start Command** a:
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
3. Guarda los cambios
4. Haz deploy

### Opción 3: Desactivar Config-as-Code

Si Railway tiene habilitado "Config-as-Code":

1. En Railway, ve a **Settings**
2. Busca la sección **"Config-as-code"**
3. Desactívala temporalmente
4. Cambia manualmente el **Start Command** en la interfaz
5. Guarda y haz deploy

## 📝 Verificación

Después de aplicar la solución:

1. Ve a **Settings** → **Deploy**
2. Verifica que **Start Command** sea:
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
3. Haz deploy
4. Verifica los logs - deberías ver:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:XXXX
   ```

## 🔄 Sincronización con GitHub

Si Railway está conectado a GitHub:

1. Los cambios en `railway.json` se aplicarán automáticamente en el próximo deploy
2. O puedes forzar un nuevo deploy haciendo un push a GitHub
3. Railway detectará los cambios y los aplicará

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

