#!/usr/bin/env python3
"""
Script para verificar la configuración de la base de datos
"""

import os
import sys
from sqlalchemy import create_engine, text
from config import Config

def check_database():
    """Verifica la conexión a la base de datos"""
    print("🔍 Verificando conexión a la base de datos...")
    
    try:
        # Crear engine
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        
        # Probar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            
            # Verificar si existe la tabla blacklist
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM blacklist"))
                count = result.scalar()
                print(f"✅ Tabla 'blacklist' existe con {count} registros")
                return True
            except Exception as e:
                print("⚠️  Tabla 'blacklist' no existe, se creará automáticamente")
                return True
                
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print("\n💡 Soluciones posibles:")
        print("1. Verificar que PostgreSQL esté corriendo")
        print("2. Verificar las credenciales en DATABASE_URL")
        print("3. Crear la base de datos 'blacklist_db'")
        return False

def show_config():
    """Muestra la configuración actual"""
    print("📋 Configuración actual:")
    print(f"   DATABASE_URL: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"   JWT_SECRET_KEY: {'*' * len(Config.JWT_SECRET_KEY) if Config.JWT_SECRET_KEY else 'NO CONFIGURADO'}")
    print(f"   SECRET_KEY: {'*' * len(Config.SECRET_KEY) if Config.SECRET_KEY else 'NO CONFIGURADO'}")

def main():
    print("🚀 Verificación de configuración de la API Blacklist")
    print("=" * 50)
    
    show_config()
    print()
    
    if check_database():
        print("\n✅ Base de datos configurada correctamente")
        print("🎯 Puedes ejecutar las pruebas con: python test_api.py")
        return 0
    else:
        print("\n❌ Problemas con la configuración de la base de datos")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)