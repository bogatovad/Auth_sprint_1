from flask_marshmallow import Marshmallow

from db.extensions import ma
from db_models import Role, User, Permission

  
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    fields = ('endpoint', 'method')

    class Meta:
        model = Permission
