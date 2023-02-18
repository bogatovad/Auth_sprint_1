from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
ma = Marshmallow()
