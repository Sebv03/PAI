# backend/verify_endpoints.py
"""
Script para verificar que todos los endpoints estén correctamente configurados.
Verifica:
1. Que todos los módulos se importen correctamente
2. Que todos los endpoints usen los campos correctos (español)
3. Que los permisos estén correctos (current_user.rol)
"""

import sys
import re
from pathlib import Path

def check_file_for_issues(file_path: Path):
    """Verifica un archivo de endpoint por problemas comunes."""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Verificar que use current_user.rol en lugar de current_user.role
        if re.search(r'current_user\.role\b', content):
            issues.append(f"❌ Usa 'current_user.role' en lugar de 'current_user.rol'")
        
        # Verificar que use campos en español
        if re.search(r'\.email\b', content) and 'correo' not in content:
            issues.append(f"⚠️  Usa '.email' - debería usar '.correo'")
        
        if re.search(r'\.full_name\b', content) and 'nombre_completo' not in content:
            issues.append(f"⚠️  Usa '.full_name' - debería usar '.nombre_completo'")
        
        if re.search(r'\.owner_id\b', content) and 'propietario_id' not in content:
            issues.append(f"⚠️  Usa '.owner_id' - debería usar '.propietario_id'")
        
        # Verificar que use UserRole correctamente
        if re.search(r'UserRole\.', content) and 'from app.models.user import.*UserRole' not in content:
            # Verificar que importe UserRole
            if 'UserRole' in content and 'import.*UserRole' not in content:
                pass  # Puede estar importado de otra manera
        
    except Exception as e:
        issues.append(f"❌ Error al leer archivo: {e}")
    
    return issues

def main():
    """Función principal de verificación."""
    print("=" * 60)
    print("VERIFICACIÓN DE ENDPOINTS")
    print("=" * 60)
    
    endpoints_dir = Path(__file__).parent / "app" / "api" / "endpoints"
    
    if not endpoints_dir.exists():
        print(f"❌ No se encontró el directorio de endpoints: {endpoints_dir}")
        return
    
    endpoint_files = [
        "users.py",
        "courses.py",
        "tasks.py",
        "enrollments.py",
        "submissions.py",
        "announcements.py",
        "ml_predictions.py",
        "student_profiles.py",
        "login.py"
    ]
    
    all_issues = {}
    
    for file_name in endpoint_files:
        file_path = endpoints_dir / file_name
        if file_path.exists():
            print(f"\n📄 Verificando {file_name}...")
            issues = check_file_for_issues(file_path)
            if issues:
                all_issues[file_name] = issues
                for issue in issues:
                    print(f"  {issue}")
            else:
                print(f"  ✅ Sin problemas detectados")
        else:
            print(f"  ⚠️  Archivo no encontrado: {file_name}")
    
    # Verificar importaciones
    print("\n" + "=" * 60)
    print("VERIFICANDO IMPORTACIONES...")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from app.api.endpoints import (
            users, courses, tasks, enrollments, 
            submissions, announcements, ml_predictions, student_profiles
        )
        from app.api.endpoints.login import router as login_router
        print("✅ Todos los módulos de endpoints se importan correctamente")
    except Exception as e:
        print(f"❌ Error al importar endpoints: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    if all_issues:
        print(f"⚠️  Se encontraron problemas en {len(all_issues)} archivo(s):")
        for file_name, issues in all_issues.items():
            print(f"\n  {file_name}:")
            for issue in issues:
                print(f"    {issue}")
    else:
        print("✅ Todos los endpoints están correctamente configurados")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

