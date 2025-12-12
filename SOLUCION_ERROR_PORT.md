# 🔧 Solución: Error "$PORT is not a valid integer"

## ❌ Problema
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

Este error ocurre porque Railway no está expandiendo la variable `$PORT` correctamente en el comando de inicio.

## ✅ Soluciones

### Solución 1: Usar el script start.sh (Recomendado)

He creado un script `backend/start.sh` que lee PORT correctamente.

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   bash start.sh
   ```
3. Guarda y haz deploy nuevamente

### Solución 2: Usar Python directamente

Si prefieres no usar el script, usa este comando:

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
3. Guarda y haz deploy nuevamente

### Solución 3: Usar comando con valor por defecto

Alternativa más simple:

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
3. Guarda y haz deploy nuevamente

## 🔍 ¿Por qué ocurre esto?

Railway proporciona la variable `PORT` automáticamente, pero a veces no expande `$PORT` correctamente en el comando. El script `start.sh` lee PORT desde las variables de entorno del sistema, que Railway siempre proporciona correctamente.

## 📝 Verificación

Después de cambiar el comando:

1. Haz clic en **"Deploy"** o presiona **Ctrl+Enter**
2. Espera a que termine el deploy
3. Verifica los logs en **"Deployments"**
4. Deberías ver algo como:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
   ```

## 🚨 Si aún no funciona

1. Verifica que el archivo `start.sh` esté en la carpeta `backend/`
2. Verifica que tenga permisos de ejecución (Railway lo maneja automáticamente)
3. Revisa los logs completos en Railway para ver el error exacto
4. Prueba la Solución 2 o 3 como alternativa

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

