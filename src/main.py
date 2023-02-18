from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from db.postgres import init_db
from api.v1.views.role import role
from db.extensions import db, ma, api

from db_models import Role


app = Flask(__name__)
app.register_blueprint(role)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


app.config.from_pyfile('./core/config', silent=True)
init_db(app)
ma.init_app(app)
api.init_app(app)
app.app_context().push()
db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
