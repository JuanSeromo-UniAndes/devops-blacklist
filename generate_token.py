from flask_jwt_extended import create_access_token
from main import app

def generate_test_token():
    with app.app_context():
        # Token estático para pruebas
        token = create_access_token(identity='test_user')
        return token

if __name__ == '__main__':
    token = generate_test_token()
    print(f"Test JWT Token: {token}")
    print("\nUse this token in Postman:")
    print(f"Authorization: Bearer {token}")