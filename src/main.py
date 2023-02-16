from flask import Flask

from db.postgres import init_db, db
from db.models import User

app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


def main():
    init_db(app)
    app.run(host='0.0.0.0', port=5555)


if __name__ == '__main__':
    main()
