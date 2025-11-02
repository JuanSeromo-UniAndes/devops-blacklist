from flask import Flask
from config import Config
from sqlalchemy.exc import OperationalError
from extensions import db, ma, jwt, api


import logging


app = Flask(__name__)
app.config.from_object(Config)


# Inicializar extensiones
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)


from resources.blacklist_resource import BlacklistResource
from resources.get_blacklist_resource import GetBlacklistResource

api.add_resource(BlacklistResource, '/blacklist')
api.add_resource(GetBlacklistResource, '/blacklist/<string:email>')

# Inicializar API después de registrar recursos
api.init_app(app)

logger = logging.getLogger(__name__)


@app.route('/')
def root():
    return 'OK'


@app.route('/blacklist/ping')
def health_check():
    return 'pong'


with app.app_context():
    try:
        db.create_all()
    except OperationalError as exc:
        logger.error("Database unavailable at startup, skipping create_all: %s", exc)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)