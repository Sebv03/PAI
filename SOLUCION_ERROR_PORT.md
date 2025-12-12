# 🔧 Solución: Error "$PORT is not a valid integer"

## ❌ Problema
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

Este error ocurre porque Railway no está expandiendo la variable `$PORT` correctamente en el comando de inicio.

## ✅ Soluciones

### Solución 1: Usar script Python start.py (Recomendado)

He creado un script `backend/start.py` que lee PORT correctamente desde las variables de entorno.

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   python start.py
   ```
3. Guarda y haz deploy nuevamente

**Nota:** Este script está en `backend/start.py` y lee PORT automáticamente desde `os.environ`.

### Solución 2: Usar comando directo con puerto fijo (Alternativa)

Si la Solución 1 no funciona, Railway asignará el puerto automáticamente:

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
3. Guarda y haz deploy nuevamente

**Nota:** Railway asignará el puerto correcto automáticamente, incluso si especificas 8000.

## 🔍 ¿Por qué ocurre esto?

Railway proporciona la variable `PORT` automáticamente, pero no expande sintaxis de shell como `${PORT:-8000}`. El script `start.py` lee PORT directamente desde `os.environ` en Python, que es la forma más confiable de acceder a variables de entorno en Railway.

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

1. Verifica que el **Root Directory** esté configurado como `backend` en Settings
2. Verifica que `requirements.txt` esté en la carpeta `backend/`
3. Revisa los logs completos en Railway para ver el error exacto
4. Prueba la Solución 2 como alternativa
5. Si Railway no reconoce `${PORT}`, intenta usar directamente el valor por defecto:
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   (Railway asignará el puerto automáticamente)

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

