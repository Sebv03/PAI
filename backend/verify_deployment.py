#!/usr/bin/env python
"""
Script para verificar que el despliegue está configurado correctamente.
Ejecuta este script después de configurar las variables de entorno en Railway.
"""
import os
import sys

def verify_environment():
    """Verifica que todas las variables de entorno necesarias estén configuradas."""
    required_vars = {
        'DATABASE_URL': 'URL de conexión a PostgreSQL',
        'SECRET_KEY': 'Clave secreta para JWT',
    }
    
    optional_vars = {
        'BACKEND_CORS_ORIGINS': 'Orígenes permitidos para CORS',
        'UPLOAD_DIR': 'Directorio para archivos subidos',
    }
    
    print("🔍 Verificando configuración del despliegue...\n")
    
    missing_required = []
    missing_optional = []
    
    # Verificar variables requeridas
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_required.append(f"  ❌ {var}: {description}")
        else:
            # Ocultar valores sensibles
            if 'PASSWORD' in var.upper() or 'SECRET' in var.upper() or 'KEY' in var.upper():
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
    
    # Verificar variables opcionales
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if not value:
            missing_optional.append(f"  ⚠️  {var}: {description} (opcional)")
        else:
            print(f"  ✅ {var}: {value}")
    
    print("\n" + "="*60)
    
    if missing_required:
        print("\n❌ ERROR: Variables de entorno requeridas faltantes:\n")
        for msg in missing_required:
            print(msg)
        print("\n💡 Configura estas variables en Railway → Service → Variables")
        return False
    
    if missing_optional:
        print("\n⚠️  ADVERTENCIA: Variables opcionales no configuradas:\n")
        for msg in missing_optional:
            print(msg)
        print("\n💡 Estas variables usarán valores por defecto.")
    
    print("\n✅ ¡Configuración verificada correctamente!")
    print("\n📝 Próximos pasos:")
    print("  1. Ejecuta: python init_db.py (para crear tablas)")
    print("  2. Ejecuta: python create_admin.py (para crear usuario admin)")
    print("  3. Verifica que el backend responda en: /docs")
    
    return True

if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)

