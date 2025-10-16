import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"

def test_health():
    """Prueba básica de health check"""
    print("Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/blacklist/ping")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_token():
    """Genera token usando el script existente"""
    print("Generando token...")
    try:
        from flask_jwt_extended import create_access_token
        from app import app
        
        with app.app_context():
            token = create_access_token(identity='test_user')
            print(f"Token: {token}")
            return token
    except Exception as e:
        print(f"Error generando token: {e}")
        return None

def test_add_email(token):
    """Prueba agregar email"""
    print("Agregando email a blacklist...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": "test@example.com",
        "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
        "blocked_reason": "Prueba local"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/blacklist", headers=headers, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_check_email(token):
    """Prueba verificar email"""
    print("Verificando email...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/blacklist/test@example.com", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Pruebas basicas de la API")
    print("=" * 40)
    
    # 1. Health check
    if not test_health():
        print("API no esta corriendo. Ejecuta python app.py primero")
        exit(1)
    
    # 2. Generar token
    token = get_token()
    if not token:
        print("No se pudo generar token")
        exit(1)
    
    # 3. Agregar email
    print("\n" + "-" * 40)
    test_add_email(token)
    
    # 4. Verificar email
    print("\n" + "-" * 40)
    test_check_email(token)
    
    print("\nPruebas completadas")