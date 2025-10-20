from flask import Flask
from config import Config
from extensions import db, ma, jwt, api

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)

# Importar recursos antes de inicializar API
from resources.blacklist_resource import BlacklistResource
from resources.get_blacklist_resource import GetBlacklistResource

# Registrar recursos
api.add_resource(BlacklistResource, '/blacklist')
api.add_resource(GetBlacklistResource, '/blacklist/<string:email>')

# Inicializar API después de registrar recursos
api.init_app(app)


@app.route('/')
def root():
    return 'OK'

@app.route('/blacklist/ping')
def health_check():
    return 'pong'


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
