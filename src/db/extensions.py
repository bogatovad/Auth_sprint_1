from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
