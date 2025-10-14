from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.blacklist import Blacklist, BlacklistSchema


blacklist_schema = BlacklistSchema()


class GetBlacklistResource(Resource):
    @jwt_required()
    def get(self, email: str):
        try:
            existing = Blacklist.query.filter_by(email=email).first()
            if existing:
                return {
                    "existing": True,
                    "blocked_reason": existing.blocked_reason
                }, 409
            if not existing:
                return {
                    "existing": False,
                }
        except Exception as e:
            return {'message': 'Error al obteber email: {}'.format(str(e))}, 500

