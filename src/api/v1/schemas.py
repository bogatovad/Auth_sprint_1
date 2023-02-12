from flask_marshmallow import Marshmallow

from db.extensions import ma
from db_models import Role

  
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


