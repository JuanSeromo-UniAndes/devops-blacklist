from flask_jwt_extended import create_access_token
from app import app

def generate_test_token():
    with app.app_context():
        token = create_access_token(identity='test_user')
        return token

if __name__ == '__main__':
    token = generate_test_token()
    print(f"Token: {token}")
    print(f"\nAuthorization: Bearer {token}")