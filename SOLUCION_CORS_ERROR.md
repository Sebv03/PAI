# 🔧 Solución: Error parsing BACKEND_CORS_ORIGINS

## ❌ Problema
```
pydantic_settings.sources.SettingsError: error parsing value for field "BACKEND_CORS_ORIGINS"
```

Pydantic Settings no puede parsear `BACKEND_CORS_ORIGINS` cuando está definido como `List[str]` directamente.

## ✅ Solución Aplicada

He cambiado `BACKEND_CORS_ORIGINS` para que sea un `str` (string separado por comas) en lugar de `List[str]`. Esto es más compatible con Pydantic Settings.

### Formato en Railway

En Railway → Variables, configura `BACKEND_CORS_ORIGINS` como:

```
BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app
```

O múltiples orígenes separados por comas:

```
BACKEND_CORS_ORIGINS=https://app1.vercel.app,https://app2.vercel.app
```

## 📝 Cambios Realizados

1. `BACKEND_CORS_ORIGINS` ahora es `str` en lugar de `List[str]`
2. Se agregó método `get_cors_origins()` que convierte el string a lista
3. `main.py` ahora usa `settings.get_cors_origins()` en lugar de `settings.BACKEND_CORS_ORIGINS`

## 🔄 Próximos Pasos

1. **Haz pull de los cambios** en Railway (o espera a que Railway detecte automáticamente)
2. **Verifica la variable** `BACKEND_CORS_ORIGINS` en Railway → Variables
3. **Asegúrate** de que sea un string, no una lista
4. **Haz deploy** nuevamente

## 🚨 Si Aún Hay Error

Si el error persiste:

1. **Elimina temporalmente** la variable `BACKEND_CORS_ORIGINS` en Railway
2. **Haz deploy** (usará el valor por defecto)
3. **Agrega** `BACKEND_CORS_ORIGINS` nuevamente como string simple
4. **Haz deploy** nuevamente

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

