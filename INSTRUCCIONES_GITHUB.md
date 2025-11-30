# 📤 Instrucciones para Subir el Proyecto a GitHub

## ✅ Estado Actual

El proyecto ya está inicializado con Git y tiene un commit inicial con todos los archivos.

## 📋 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub

1. Ve a [GitHub.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** en la esquina superior derecha
3. Selecciona **"New repository"**
4. Completa el formulario:
   - **Repository name**: `PAI-Platform` (o el nombre que prefieras)
   - **Description**: "Plataforma Académica Inteligente para preparación PAES"
   - **Visibility**: 
     - ✅ **Public** (si quieres que sea público)
     - ✅ **Private** (si quieres que sea privado)
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
   - **NO agregues** .gitignore ni licencia (ya los tenemos)
5. Haz clic en **"Create repository"**

### 2. Conectar el Repositorio Local con GitHub

Después de crear el repositorio, GitHub te mostrará instrucciones. Ejecuta estos comandos:

```bash
cd /Users/sebahenriquez/Desktop/PAI-Platform-main

# Agregar el remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/PAI-Platform.git

# O si prefieres usar SSH:
# git remote add origin git@github.com:TU_USUARIO/PAI-Platform.git

# Verificar que se agregó correctamente
git remote -v
```

### 3. Subir el Código a GitHub

```bash
# Cambiar a la rama main (si no estás en ella)
git branch -M main

# Subir el código
git push -u origin main
```

Si te pide autenticación:
- **HTTPS**: Usa un Personal Access Token (ver sección de autenticación abajo)
- **SSH**: Asegúrate de tener tu clave SSH configurada

### 4. Verificar

Ve a tu repositorio en GitHub y verifica que todos los archivos estén ahí.

## 🔐 Autenticación con GitHub

### Opción 1: Personal Access Token (HTTPS)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Haz clic en **"Generate new token (classic)"**
3. Dale un nombre (ej: "PAI Platform")
4. Selecciona los scopes: `repo` (todos los permisos de repositorio)
5. Haz clic en **"Generate token"**
6. **Copia el token** (solo se muestra una vez)
7. Cuando Git te pida la contraseña, usa el token en lugar de tu contraseña

### Opción 2: SSH (Recomendado)

1. Genera una clave SSH si no tienes una:
```bash
ssh-keygen -t ed25519 -C "tu_email@ejemplo.com"
```

2. Agrega la clave a tu agente SSH:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

3. Copia tu clave pública:
```bash
cat ~/.ssh/id_ed25519.pub
```

4. Ve a GitHub → Settings → SSH and GPG keys → New SSH key
5. Pega tu clave pública y guarda

## 🔄 Comandos Útiles para el Futuro

### Ver el estado del repositorio
```bash
git status
```

### Agregar cambios
```bash
git add .
# O archivos específicos:
git add archivo1.py archivo2.js
```

### Hacer commit
```bash
git commit -m "Descripción de los cambios"
```

### Subir cambios
```bash
git push
```

### Ver historial de commits
```bash
git log --oneline
```

### Crear una nueva rama
```bash
git checkout -b nombre-de-la-rama
```

### Cambiar de rama
```bash
git checkout main
```

## ⚠️ Archivos que NO se Suben

El archivo `.gitignore` está configurado para NO subir:
- ✅ Entornos virtuales (`venv/`)
- ✅ `node_modules/`
- ✅ Archivos `.env` con credenciales
- ✅ Archivos subidos (`uploads/`)
- ✅ Archivos de caché (`__pycache__/`)
- ✅ Modelos entrenados grandes (opcional)

## 📝 Notas Importantes

1. **No subir credenciales**: Asegúrate de que `.env` esté en `.gitignore`
2. **Modelos ML**: El modelo `.pkl` se sube por defecto. Si es muy grande, puedes agregarlo al `.gitignore`
3. **Base de datos**: Nunca subas archivos de base de datos (`.db`, `.sqlite`)

## 🆘 Solución de Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/PAI-Platform.git
```

### Error: "failed to push some refs"
```bash
# Primero hacer pull
git pull origin main --allow-unrelated-histories
# Luego push
git push -u origin main
```

### Error de autenticación
- Verifica que tu token SSH/HTTPS esté configurado correctamente
- Revisa la sección de autenticación arriba

---

¡Listo! Tu proyecto debería estar en GitHub ahora. 🎉

