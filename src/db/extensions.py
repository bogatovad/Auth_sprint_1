from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
api = Api()
migrate = Migrate()
oauth_client = OAuth()

