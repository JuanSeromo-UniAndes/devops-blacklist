from main import app

def test_routes():
    """Verificar que las rutas se registraron correctamente"""
    with app.app_context():
        print("Rutas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.methods} {rule.rule}")

if __name__ == "__main__":
    test_routes()