from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from main import db
from models.blacklist import Blacklist, BlacklistSchema
from werkzeug.wrappers import Response
import json

blacklist_schema = BlacklistSchema()


class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {'message': 'No se proporcionaron datos'}, 400

            email = data.get('email')
            app_uuid = data.get('app_uuid')
            blocked_reason = data.get('blocked_reason')

            if not all([email, app_uuid, blocked_reason]):
                response_data = json.dumps({'message': 'Faltan campos requeridos: email, app_uuid, blocked_reason'})
                return Response(response_data, status=400, mimetype='application/json')

            # Verificar si ya existe
            existing = Blacklist.query.filter_by(email=email, app_uuid=app_uuid).first()
            if existing:
                return {'message': 'La entrada ya existe en la blacklist'}, 409

            new_entry = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason)
            db.session.add(new_entry)
            db.session.commit()

            response_data = json.dumps({'message': 'Entrada creada exitosamente en la blacklist'})
            return Response(response_data, status=201, mimetype='application/json')

        except Exception as e:
            response_data = json.dumps({'message': f'Error al crear la entrada: {str(e)}'})
            return Response(response_data, status=500, mimetype='application/json')