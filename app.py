from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Api, Resource
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
import uuid
import re

# Configuración
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blacklist.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'

# Inicialización
app = Flask(__name__)
app.config.from_object(Config)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)

# Modelo
class Blacklist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False)
    app_uuid: Mapped[str] = mapped_column(db.String(36), nullable=False)
    blocked_reason: Mapped[str] = mapped_column(db.String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(db.String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email, app_uuid, blocked_reason, ip_address):
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason or "No reason provided"
        self.ip_address = ip_address
        self.created_at = datetime.utcnow()

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist

blacklist_schema = BlacklistSchema()

# Recursos
class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400

            email = data.get('email')
            app_uuid = data.get('app_uuid')
            blocked_reason = data.get('blocked_reason', '')

            if not email or not app_uuid:
                return {'message': 'Missing required fields: email, app_uuid'}, 400

            # Validar formato de email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return {'message': 'Invalid email format'}, 400

            # Validar UUID
            try:
                uuid.UUID(app_uuid)
            except ValueError:
                return {'message': 'Invalid UUID format for app_uuid'}, 400

            # Obtener IP del cliente
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
            if ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()

            # Verificar si ya existe
            existing = Blacklist.query.filter_by(email=email).first()
            if existing:
                return {'message': 'Email already exists in blacklist'}, 400

            new_entry = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, ip_address=client_ip)
            db.session.add(new_entry)
            db.session.commit()

            return {'message': 'Email successfully added to blacklist'}, 201

        except Exception as e:
            return {'message': f'Error creating blacklist entry: {str(e)}'}, 500

class GetBlacklistResource(Resource):
    @jwt_required()
    def get(self, email: str):
        try:
            existing = Blacklist.query.filter_by(email=email).first()
            if existing:
                return {
                    "existing": True,
                    "blocked_reason": existing.blocked_reason
                }, 200
            else:
                return {
                    "existing": False
                }, 200
        except Exception as e:
            return {'message': f'Error retrieving email: {str(e)}'}, 500

# Rutas
api.add_resource(BlacklistResource, '/blacklist')
api.add_resource(GetBlacklistResource, '/blacklist/<string:email>')

@app.route('/blacklist/ping')
def health_check():
    return 'pong'

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("Iniciando API Blacklist en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)