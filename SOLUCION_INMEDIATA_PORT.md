# ⚡ Solución Inmediata: Error de PORT en Railway

## 🚨 Problema Actual
Railway está intentando ejecutar `python start.py` pero el archivo no existe en la ruta correcta.

## ✅ Solución Rápida (2 minutos)

### Paso 1: Cambiar Start Command Manualmente

1. Ve a Railway → Tu servicio PAI → **Settings**
2. Ve a la sección **"Deploy"**
3. En **"Start Command"**, reemplaza TODO con:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. **Guarda** los cambios (botón "Save" o Ctrl+S)
5. Haz clic en **"Deploy"** o presiona **Ctrl+Enter**

### Paso 2: Verificar

Después del deploy, en los logs deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🔍 ¿Por qué funciona?

- Railway asignará el puerto correcto automáticamente
- No necesitas leer PORT manualmente
- Railway redirige el tráfico al puerto correcto

## 📝 Nota Importante

**NO uses `$PORT` ni `${PORT}`** - Railway a veces no los expande correctamente. Usa el puerto fijo `8000` y Railway lo manejará automáticamente.

---

**¿Funcionó?** Si ves "Uvicorn running" en los logs, ¡estás listo! 🎉

