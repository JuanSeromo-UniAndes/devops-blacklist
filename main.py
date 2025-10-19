from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

jwt = JWTManager(app)
api = Api(app)

from resources.blacklist_resource import BlacklistResource
from resources.get_blacklist_resource import GetBlacklistResource

api.add_resource(BlacklistResource, '/blacklist')
api.add_resource(GetBlacklistResource, '/blacklist/<string:email>')


@app.route('/')
def root():
    return 'OK'

@app.route('/blacklist/ping')
def health_check():
    return 'pong'


with app.app_context():
    db.create_all()
