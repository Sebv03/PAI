# 🔧 Solución: "can't open file '/app/start.py'"

## ❌ Problema
```
python: can't open file '/app/start.py': [Errno 2] No such file or directory
```

Railway está buscando el archivo en `/app/` pero el Root Directory está configurado como `backend`.

## ✅ Solución Más Simple (Recomendada)

Usa el comando directo de uvicorn. Railway asignará el puerto automáticamente:

1. En Railway, ve a **Settings** → **Deploy**
2. Cambia **Start Command** a:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Si `$PORT` no funciona, usa:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Guarda y haz deploy

**Nota:** Railway asignará el puerto correcto automáticamente, incluso si especificas 8000.

## 🔍 ¿Por qué funciona?

Railway:
- Proporciona la variable `PORT` automáticamente
- Asigna el puerto correcto al servicio, incluso si especificas uno diferente
- Redirige el tráfico al puerto correcto

## 📝 Verificación

Después del deploy, en los logs deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

## 🚨 Si aún no funciona

1. Verifica que el **Root Directory** esté configurado como `backend` en Settings
2. Verifica que `app/main.py` exista en `backend/app/main.py`
3. Revisa los logs completos en Railway para ver el error exacto
4. Prueba con el puerto fijo 8000 primero

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

