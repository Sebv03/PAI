# 🎓 Plataforma Académica Inteligente (PAI)

Plataforma educativa pre-universitaria para estudiantes de 1ro a 4to medio, enfocada en la preparación para la PAES (Prueba de Acceso a la Educación Superior).

## 📋 Características Principales

- ✅ **Gestión de Cursos**: Docentes pueden crear y gestionar cursos relacionados con temáticas PAES
- ✅ **Sistema de Tareas**: Creación, entrega y calificación de tareas
- ✅ **Dashboard Personalizado**: Diferentes vistas para estudiantes, docentes y administradores
- ✅ **Foro/Comunicados**: Sistema de comunicación entre docentes y estudiantes
- ✅ **Predicción de Riesgo Académico**: Modelo ML que predice el riesgo de bajo rendimiento
- ✅ **Perfiles de Estudiantes**: Cuestionario para caracterizar el perfil académico
- ✅ **Interfaz en Español**: Toda la plataforma está traducida al español

## 🏗️ Arquitectura

### Backend
- **Framework**: FastAPI (Python)
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy

### Frontend
- **Framework**: React + Vite
- **Estado**: Zustand
- **Estilos**: CSS personalizado

### ML Service
- **Framework**: FastAPI (Microservicio)
- **Modelo**: Random Forest Classifier
- **Features**: 12 características (8 del cuestionario + 4 transaccionales)

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+ (puerto 5433)
- npm o yarn

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd PAI-Platform-main
```

2. **Configurar Base de Datos**
```bash
# Crear base de datos
./create_database.sh postgres

# La contraseña por defecto es: 123
# El puerto por defecto es: 5433
```

3. **Configurar Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Configurar ML Service**
```bash
cd ml-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configurar Frontend**
```bash
cd frontend
npm install
```

6. **Iniciar Servicios**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
./start_backend.sh
# O manualmente:
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - ML Service:**
```bash
cd ml-service
source venv/bin/activate
./start_ml_service.sh
# O manualmente:
uvicorn main:app --reload --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Acceso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **ML Service**: http://localhost:8001
- **Documentación API**: http://localhost:8000/docs

## 👥 Usuarios por Defecto

### Administrador
- **Correo**: `admin@pai.cl`
- **Contraseña**: (crear con `python backend/create_admin.py`)

### Profesores
- `patricia.morales@paes.cl`
- `roberto.gonzalez@paes.cl`
- `maria.vega@paes.cl`
- `carlos.fernandez@paes.cl`

### Estudiantes
- `estudiante1@paes.cl` hasta `estudiante50@paes.cl`
- **Contraseña**: (verificar en base de datos o scripts de población)

## 📊 Modelo ML

El modelo de predicción de riesgo académico utiliza:
- **12 Features**: 8 del cuestionario de perfil + 4 transaccionales
- **Algoritmo**: Random Forest Classifier
- **Métricas**:
  - Accuracy: ~80%
  - Precision: ~84%
  - Recall: ~80%
  - F1-Score: ~75%

Ver `REPORTE_CLASIFICACION_ML.md` para detalles completos.

## 📁 Estructura del Proyecto

```
PAI-Platform-main/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints
│   │   ├── core/        # Configuración
│   │   ├── crud/        # Operaciones BD
│   │   ├── models/      # Modelos SQLAlchemy
│   │   ├── schemas/     # Schemas Pydantic
│   │   └── services/    # Servicios
│   └── requirements.txt
├── frontend/            # Aplicación React
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── pages/       # Páginas
│   │   └── services/    # Servicios API
│   └── package.json
├── ml-service/          # Microservicio ML
│   ├── services/        # Lógica ML
│   └── models/          # Modelos entrenados
└── datasets/            # Datos históricos
```

## 🔧 Configuración

### Variables de Entorno

**Backend** (`backend/app/core/config.py`):
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `SECRET_KEY`: Clave secreta para JWT
- `BACKEND_CORS_ORIGINS`: Orígenes permitidos para CORS

**ML Service** (`ml-service/core/config.py`):
- `DATABASE_URL`: URL de conexión a PostgreSQL (misma que backend)

## 📚 Documentación

- `INSTRUCCIONES_LOCALES.md`: Guía de instalación local
- `ANALISIS_ENFOQUE_RECOMENDACIONES.md`: Análisis de sistema de recomendaciones
- `REPORTE_CLASIFICACION_ML.md`: Reporte detallado del modelo ML
- `GUIA_POSTMAN.md`: Guía para probar la API con Postman

## 🧪 Testing

### Verificar Endpoints
```bash
cd backend
source venv/bin/activate
python verify_endpoints.py
```

### Generar Reporte ML
```bash
cd ml-service
source venv/bin/activate
python get_classification_report.py
```

## 🚢 Despliegue

Ver `GUIA_DESPLIEGUE.md` para instrucciones de despliegue en producción.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de uso educativo.

## 👨‍💻 Autor

Desarrollado para plataforma educativa pre-universitaria.

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- React por la librería de UI
- Scikit-learn por las herramientas de ML

---

**Versión**: 1.0.0
**Última actualización**: 2025-11-30

