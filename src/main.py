from flask import Flask
from flask_restful import Api
from api.v1.urls import urls
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from db.postgres import init_db


app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

swag = Swagger(app)

for resource, url in urls:
    api.add_resource(resource, url)


def main():
    init_db(app)
    app.run(host="0.0.0.0", port=5555)


if __name__ == "__main__":
    main()
