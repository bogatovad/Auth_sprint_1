from flask import Flask
from api.v1.views.role.role import role


app = Flask(__name__)
app.register_blueprint(role)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
