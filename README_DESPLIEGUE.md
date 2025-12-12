# 🚀 Guía Completa de Despliegue en Internet (GRATIS)

Esta es la guía principal para desplegar tu plataforma PAI completamente en internet usando servicios gratuitos.

## 📚 Documentos Disponibles

1. **`GUIA_DESPLIEGUE_GRATUITO.md`** - Guía detallada paso a paso (leer primero)
2. **`DESPLIEGUE_RAPIDO.md`** - Resumen ejecutivo de 7 pasos
3. Este archivo - Visión general

## 🎯 Opciones de Despliegue

### Opción 1: Railway + Vercel (Recomendado - Más Fácil)
- ✅ Backend: Railway
- ✅ Base de Datos: Railway PostgreSQL
- ✅ Frontend: Vercel
- 💰 Costo: **GRATIS** (tier gratuito suficiente)

### Opción 2: Render + Vercel (Alternativa)
- ✅ Backend: Render
- ✅ Base de Datos: Render PostgreSQL
- ✅ Frontend: Vercel
- 💰 Costo: **GRATIS** (tier gratuito)

## 📋 Requisitos Previos

- [ ] Cuenta de GitHub (para conectar repos)
- [ ] Código subido a un repositorio de GitHub
- [ ] 20-30 minutos de tu tiempo

## 🚀 Inicio Rápido

1. **Lee la guía detallada**: Abre `GUIA_DESPLIEGUE_GRATUITO.md`
2. **O sigue el resumen**: Abre `DESPLIEGUE_RAPIDO.md`
3. **Comienza con Railway**: Crear cuenta en https://railway.app
4. **Continúa con Vercel**: Crear cuenta en https://vercel.com

## 🔑 Variables Importantes

### Backend (Railway)
```
DATABASE_URL=postgresql://...
SECRET_KEY=tu_clave_secreta
BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app
```

### Frontend (Vercel)
```
VITE_API_BASE_URL=https://tu-backend.railway.app
```

## ✅ Checklist de Despliegue

- [ ] Cuenta Railway creada
- [ ] Base de datos PostgreSQL creada en Railway
- [ ] Backend desplegado en Railway
- [ ] Variables de entorno configuradas en Railway
- [ ] URL del backend obtenida
- [ ] Cuenta Vercel creada
- [ ] Frontend desplegado en Vercel
- [ ] Variables de entorno configuradas en Vercel
- [ ] CORS actualizado con URL de frontend
- [ ] Tablas de BD creadas (ejecutar `init_db.py`)
- [ ] Usuario admin creado (ejecutar `create_admin.py`)
- [ ] Verificación final: Login funciona ✅

## 🆘 ¿Problemas?

Consulta la sección "Solución de Problemas" en `GUIA_DESPLIEGUE_GRATUITO.md`

## 📞 Recursos Útiles

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Vite Docs: https://vitejs.dev

---

**¿Listo para empezar?** Abre `GUIA_DESPLIEGUE_GRATUITO.md` y sigue los pasos! 🚀

