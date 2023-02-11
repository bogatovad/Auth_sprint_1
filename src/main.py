from flask import Flask
from flask_restful import Api
from src.api.v1.urls import urls
from flask_jwt_extended import JWTManager

app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

for resource, url in urls:
    api.add_resource(resource, url)

if __name__ == '__main__':
    app.run()
