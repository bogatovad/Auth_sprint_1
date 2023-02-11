from flask import Flask

from db.postgres import init_db, db
from api.v1.views.role import role


app = Flask(__name__)
app.register_blueprint(role)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'

app.config.from_pyfile('settings.py', silent=True)
init_db(app)
app.app_context().push()
db.create_all()


if __name__ == '__main__':
    app.run()
