from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api

from api.v1.urls import urls
from api.v1.views.role import role

from .containers import ApplicationContainer


def create_app():
    """Create and return Flask application."""
    container = ApplicationContainer()

    app = container.app()
    app.container = container

    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.register_blueprint(role)
    api = Api(app)
    jwt = JWTManager(app)

    for resource, url in urls:
        api.add_resource(resource, url)

    return app
