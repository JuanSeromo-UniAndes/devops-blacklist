from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.blacklist import Blacklist, BlacklistSchema
import uuid
import re

blacklist_schema = BlacklistSchema()


class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        from main import db
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
                return {'message': 'Email already exists in blacklist'}, 409

            new_entry = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, ip_address=client_ip)
            db.session.add(new_entry)
            db.session.commit()

            return {'message': 'Email successfully added to blacklist'}, 201

        except Exception as e:
            return {'message': f'Error creating blacklist entry: {str(e)}'}, 500