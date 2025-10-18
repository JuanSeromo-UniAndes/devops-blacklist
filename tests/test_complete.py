import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"

def test_health():
    print("1. Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/blacklist/ping")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_post_no_token():
    print("2. Probando POST sin token...")
    try:
        response = requests.post(f"{BASE_URL}/blacklist", 
                               headers={"Content-Type": "application/json"},
                               json={"email": "test@example.com"})
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        return response.status_code in [401, 422]  # Esperamos error de auth
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_get_no_token():
    print("3. Probando GET sin token...")
    try:
        response = requests.get(f"{BASE_URL}/blacklist/test@example.com")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        return response.status_code in [401, 422]  # Esperamos error de auth
    except Exception as e:
        print(f"   Error: {e}")
        return False

if __name__ == "__main__":
    print("Probando endpoints de la API...")
    print("=" * 40)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("POST sin token", test_post_no_token()))
    results.append(("GET sin token", test_get_no_token()))
    
    print("\n" + "=" * 40)
    print("RESULTADOS:")
    for test_name, result in results:
        status = "OK" if result else "FAIL"
        print(f"  {status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {passed}/{len(results)} pruebas pasaron")