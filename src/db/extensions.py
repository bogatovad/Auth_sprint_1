from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
api = Api()
migrate = Migrate()
