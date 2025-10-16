#!/usr/bin/env python3
"""
Script de pruebas completo para la API Blacklist
Prueba todos los endpoints y funcionalidades implementadas
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "test@example.com"
TEST_APP_UUID = "550e8400-e29b-41d4-a716-446655440000"

def get_test_token():
    """Genera un token JWT para las pruebas"""
    try:
        from flask_jwt_extended import create_access_token
        from main import app
        
        with app.app_context():
            token = create_access_token(identity='test_user')
            return token
    except Exception as e:
        print(f"❌ Error generando token: {e}")
        return None

def test_health_check():
    """Prueba el endpoint de health check"""
    print("🔍 Probando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/blacklist/ping")
        if response.status_code == 200 and response.text == "pong":
            print("✅ Health Check: OK")
            return True
        else:
            print(f"❌ Health Check falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en Health Check: {e}")
        return False

def test_add_to_blacklist(token):
    """Prueba agregar email a la blacklist"""
    print("🔍 Probando agregar email a blacklist...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": TEST_EMAIL,
        "app_uuid": TEST_APP_UUID,
        "blocked_reason": "Prueba automatizada"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/blacklist", 
                               headers=headers, 
                               json=data)
        
        if response.status_code == 201:
            print("✅ Email agregado a blacklist correctamente")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error agregando email: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en agregar email: {e}")
        return False

def test_check_blacklisted_email(token):
    """Prueba verificar email en blacklist"""
    print("🔍 Probando verificar email blacklisteado...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/blacklist/{TEST_EMAIL}", 
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("existing") == True:
                print("✅ Email encontrado en blacklist")
                print(f"   Razón: {data.get('blocked_reason', 'N/A')}")
                return True
            else:
                print("❌ Email no encontrado en blacklist (debería estar)")
                return False
        else:
            print(f"❌ Error verificando email: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error verificando email: {e}")
        return False

def test_check_non_blacklisted_email(token):
    """Prueba verificar email NO en blacklist"""
    print("🔍 Probando verificar email NO blacklisteado...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    test_email = "notblacklisted@example.com"
    
    try:
        response = requests.get(f"{BASE_URL}/blacklist/{test_email}", 
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("existing") == False:
                print("✅ Email correctamente NO encontrado en blacklist")
                return True
            else:
                print("❌ Email encontrado en blacklist (no debería estar)")
                return False
        else:
            print(f"❌ Error verificando email: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error verificando email: {e}")
        return False

def test_duplicate_email(token):
    """Prueba agregar email duplicado"""
    print("🔍 Probando agregar email duplicado...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": TEST_EMAIL,
        "app_uuid": TEST_APP_UUID,
        "blocked_reason": "Segundo intento"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/blacklist", 
                               headers=headers, 
                               json=data)
        
        if response.status_code == 400:
            print("✅ Email duplicado correctamente rechazado")
            return True
        else:
            print(f"❌ Email duplicado no rechazado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando duplicado: {e}")
        return False

def test_unauthorized_access():
    """Prueba acceso sin token"""
    print("🔍 Probando acceso sin autorización...")
    
    try:
        # Sin token
        response = requests.get(f"{BASE_URL}/blacklist/{TEST_EMAIL}")
        
        if response.status_code == 401:
            print("✅ Acceso sin token correctamente rechazado")
            return True
        else:
            print(f"❌ Acceso sin token no rechazado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando acceso no autorizado: {e}")
        return False

def test_invalid_token():
    """Prueba con token inválido"""
    print("🔍 Probando token inválido...")
    
    headers = {
        "Authorization": "Bearer invalid_token_here"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/blacklist/{TEST_EMAIL}", 
                              headers=headers)
        
        if response.status_code == 422:  # JWT decode error
            print("✅ Token inválido correctamente rechazado")
            return True
        else:
            print(f"❌ Token inválido no rechazado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando token inválido: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la API Blacklist")
    print("=" * 50)
    
    # Verificar que el servidor esté corriendo
    if not test_health_check():
        print("\n❌ El servidor no está corriendo. Ejecuta: python main.py")
        sys.exit(1)
    
    # Generar token
    print("\n🔑 Generando token de prueba...")
    token = get_test_token()
    if not token:
        print("❌ No se pudo generar el token")
        sys.exit(1)
    print(f"✅ Token generado: {token[:50]}...")
    
    # Ejecutar pruebas
    tests = [
        ("Acceso sin autorización", test_unauthorized_access),
        ("Token inválido", test_invalid_token),
        ("Agregar email a blacklist", lambda: test_add_to_blacklist(token)),
        ("Verificar email blacklisteado", lambda: test_check_blacklisted_email(token)),
        ("Verificar email NO blacklisteado", lambda: test_check_non_blacklisted_email(token)),
        ("Email duplicado", lambda: test_duplicate_email(token))
    ]
    
    results = []
    print("\n" + "=" * 50)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)