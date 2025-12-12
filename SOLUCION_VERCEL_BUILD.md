# 🔧 Solución: Error de Build en Vercel

## ❌ Problema
```
Error: Command "cd frontend && npm install && npm run build" exited with 1
```

## ✅ Solución

### Paso 1: Configurar Vercel Correctamente

En Vercel, cuando importes el proyecto:

1. **Framework Preset**: Selecciona **"Vite"** (o déjalo en "Other")
2. **Root Directory**: `frontend` ⚠️ **MUY IMPORTANTE**
3. **Build Command**: `npm run build` (o déjalo vacío, Vercel lo detectará)
4. **Output Directory**: `dist` (o déjalo vacío, Vercel lo detectará)
5. **Install Command**: `npm install` (o déjalo vacío)

### Paso 2: Variables de Entorno

En la sección **"Environment Variables"**, agrega:

```
VITE_API_BASE_URL=https://tu-backend-url.railway.app
```

**Importante:** Reemplaza con la URL real de tu backend de Railway.

### Paso 3: Si el Build Falla por TypeScript

Si ves errores de TypeScript, puedes:

**Opción A:** Desactivar la verificación de tipos en el build (temporal):

1. En Vercel, ve a **Settings** → **Build & Development Settings**
2. Cambia **Build Command** a:
   ```
   npm run build -- --mode production
   ```
   O modifica `frontend/package.json` temporalmente:
   ```json
   "build": "vite build"
   ```
   (sin `tsc -b`)

**Opción B:** Corregir los errores de TypeScript:

1. Revisa los logs de build en Vercel
2. Corrige los errores de TypeScript que aparezcan
3. Haz commit y push
4. Vercel desplegará automáticamente

### Paso 4: Verificar Configuración

Asegúrate de que:

- ✅ **Root Directory** está configurado como `frontend`
- ✅ `package.json` está en `frontend/package.json`
- ✅ `vite.config.js` está en `frontend/vite.config.js`
- ✅ `VITE_API_BASE_URL` está configurada en Variables de Entorno

## 🔍 Errores Comunes

### Error: "Cannot find module"
- Verifica que **Root Directory** sea `frontend`
- Verifica que `node_modules` no esté en `.gitignore` (debe estar)

### Error: "TypeScript errors"
- Temporalmente cambia el build command a solo `vite build`
- O corrige los errores de TypeScript

### Error: "VITE_API_BASE_URL is not defined"
- Verifica que la variable esté en **Environment Variables** de Vercel
- Verifica que el nombre sea exactamente `VITE_API_BASE_URL` (con VITE_ al inicio)

## 📝 Configuración Recomendada en Vercel

```
Framework Preset: Vite
Root Directory: frontend
Build Command: (vacío - Vercel lo detecta)
Output Directory: (vacío - Vercel lo detecta)
Install Command: (vacío - Vercel lo detecta)
```

**Variables de Entorno:**
```
VITE_API_BASE_URL=https://tu-backend.railway.app
```

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

