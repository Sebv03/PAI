# ⚡ Despliegue Rápido - Resumen Ejecutivo

## 🎯 Pasos Rápidos (15-20 minutos)

### 1. Preparación (2 min)
```bash
# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Railway - Base de Datos (3 min)
1. https://railway.app → Login → New Project → Empty Project
2. + New → Database → Add PostgreSQL
3. Copiar `DATABASE_URL` de Variables

### 3. Railway - Backend (5 min)
1. + New → GitHub Repo → Seleccionar repo
2. Settings:
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Variables:
   ```
   DATABASE_URL=<copiada_del_paso_2>
   SECRET_KEY=<generada_en_paso_1>
   BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app
   ```
4. Settings → Generate Domain → Copiar URL del backend

### 4. Vercel - Frontend (5 min)
1. https://vercel.com → Login → Add New → Project
2. Importar repo
3. Configurar:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Variables:
   ```
   VITE_API_BASE_URL=<url_del_backend_railway>
   ```
5. Deploy → Copiar URL del frontend

### 5. Actualizar CORS (1 min)
- Railway → Backend → Variables → Actualizar `BACKEND_CORS_ORIGINS` con URL de Vercel

### 6. Crear Tablas (2 min)
```bash
# Opción A: Railway CLI
railway link
railway run python backend/init_db.py

# Opción B: Local
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Crear .env con DATABASE_URL de Railway
python init_db.py
python create_admin.py
```

### 7. Verificar (1 min)
- Abrir frontend de Vercel
- Hacer login con admin creado
- ✅ ¡Listo!

---

## 📝 URLs Necesarias

Guarda estas URLs:
- ✅ Backend: `https://xxx.railway.app`
- ✅ Frontend: `https://xxx.vercel.app`
- ✅ Database URL: `postgresql://...`

---

## 🔧 Comandos Útiles

```bash
# Ver logs de Railway
railway logs

# Conectar a base de datos localmente
railway connect postgres

# Reiniciar servicio
# Railway Dashboard → Service → Settings → Restart
```

---

**¿Problemas?** Ver `GUIA_DESPLIEGUE_GRATUITO.md` para solución detallada.

