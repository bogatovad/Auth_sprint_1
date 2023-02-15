"""Extensions registry"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
api = Api()
