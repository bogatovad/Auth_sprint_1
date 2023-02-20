from flask_jwt_extended import JWTManager
from flask_restful import Api
from flasgger import Swagger
from core.config import ACCESS_TOKEN_EXPERATION_TIMEDELTA, REFRESH_TOKEN_EXPIRATION_TIMEDELTA
from api.v1.urls import urls

from .containers import ApplicationContainer
from flask_marshmallow import Marshmallow


def create_app():
    """Create and return Flask application."""
    container = ApplicationContainer()

    app = container.app()
    app.container = container

    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_TOKEN_EXPERATION_TIMEDELTA
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_TOKEN_EXPIRATION_TIMEDELTA
    api = Api(app)
    jwt = JWTManager(app)
    swag = Swagger(app)  # host:port/apidocs/

    for resource, url in urls:
        api.add_resource(resource, url)

    return app
