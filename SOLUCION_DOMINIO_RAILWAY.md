# 🔧 Solución: No se genera el dominio en Railway

## ❌ Problema
Al hacer clic en "Generate Domain" o en el campo "Public domain will be generated", no aparece la URL.

## ✅ Solución Paso a Paso

### Paso 1: Verificar que el servicio esté desplegado

1. En Railway, ve a la pestaña **"Deployments"** (arriba, junto a Settings)
2. Verifica que haya un deployment **exitoso** (debe tener un check verde ✅)
3. Si no hay deployment o está fallando, continúa con el Paso 2

### Paso 2: Hacer el Deploy

1. En Railway, en la parte superior izquierda, verás un botón morado **"Deploy"** con una flecha hacia arriba
2. Haz clic en **"Deploy"** o presiona **Ctrl+Enter** (Windows) / **Cmd+Enter** (Mac)
3. Espera 2-5 minutos mientras Railway:
   - Construye tu aplicación
   - Instala dependencias
   - Inicia el servicio
4. Verás el progreso en tiempo real

### Paso 3: Verificar que el Deploy fue exitoso

1. Ve a la pestaña **"Deployments"**
2. Busca el deployment más reciente
3. Debe mostrar:
   - ✅ Estado: "Success" o "Active"
   - 🟢 Indicador verde
4. Si hay errores (rojo), haz clic en el deployment para ver los logs

### Paso 4: Generar el Dominio (AHORA SÍ)

**Solo después de que el deploy esté exitoso:**

1. Ve a la pestaña **"Settings"**
2. Desplázate hasta la sección **"Networking"**
3. En **"Public Networking"**, verás:
   - Un campo que dice "Public domain will be generated"
   - Un ícono de globo 🌐
4. Haz clic en el **ícono de globo** o en el campo mismo
5. Railway generará automáticamente un dominio como:
   - `https://pai-production-xxxx.up.railway.app`
   - `https://pai-production.up.railway.app`

### Paso 5: Copiar la URL

1. Una vez generado, verás la URL completa en el campo
2. Haz clic en la URL para copiarla
3. O selecciona el texto y copia (Ctrl+C)
4. **¡GUARDA ESTA URL!** La necesitarás para:
   - Configurar el frontend en Vercel
   - Actualizar CORS

---

## 🔍 Verificar Configuración

Si aún no funciona, verifica:

### 1. Root Directory está configurado
- Settings → Build → Root Directory debe ser: `backend`

### 2. Start Command está correcto
- Settings → Deploy → Start Command debe ser:
  ```
  python start.py
  ```
  O alternativamente (si el script no funciona):
  ```
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

### 3. Variables de Entorno están configuradas
- Settings → Variables debe tener:
  - `DATABASE_URL`
  - `SECRET_KEY`
  - `BACKEND_CORS_ORIGINS` (puede ser temporal por ahora)

### 4. El servicio está "Online"
- En la tarjeta del servicio PAI, debe decir "Online" con un punto verde

---

## 🚨 Errores Comunes

### Error: "Build failed"
- Revisa los logs en Deployments
- Verifica que `requirements.txt` esté en la carpeta `backend/`
- Verifica que `Root Directory` sea `backend`

### Error: "Service failed to start"
- Revisa los logs
- Verifica que `Start Command` sea correcto
- Verifica que `DATABASE_URL` esté configurada

### Error: "No domain generated"
- **Asegúrate de que el deploy esté completo y exitoso**
- Espera 1-2 minutos después del deploy
- Intenta refrescar la página (F5)
- Ve a Settings → Networking y haz clic en "Generate Domain" manualmente

---

## 📝 Orden Correcto de Pasos

1. ✅ Configurar Settings (Root Directory, Start Command)
2. ✅ Configurar Variables de Entorno
3. ✅ **Hacer Deploy** (botón "Deploy" o Ctrl+Enter)
4. ✅ Esperar a que el deploy termine exitosamente
5. ✅ Ir a Settings → Networking
6. ✅ Generar dominio (hacer clic en el ícono de globo)
7. ✅ Copiar la URL generada

---

## 💡 Consejo

**El dominio solo se genera DESPUÉS de un deploy exitoso.** Si no has hecho deploy aún, Railway no puede generar el dominio porque no hay un servicio corriendo.

---

## 🆘 Si Nada Funciona

1. Verifica los logs en la pestaña **"Deployments"**
2. Verifica que el servicio esté "Online" (punto verde)
3. Intenta hacer un nuevo deploy
4. Contacta el soporte de Railway si el problema persiste

---

**¿Necesitas más ayuda?** Revisa `GUIA_DESPLIEGUE_GRATUITO.md` para la guía completa.

