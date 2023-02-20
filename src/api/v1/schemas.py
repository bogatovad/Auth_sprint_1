from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

from db.extensions import ma


class PermissionSchemaOut(Schema):
    resource = fields.String()
    method = fields.String()


class RoleSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    name = fields.String()
    permissions = fields.Nested(PermissionSchemaOut, many=True)


class DeviceSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    name = fields.String()


class HistorySchemaOut(Schema):
    """Схема для возвращения истории авторизации пользователя."""

    date_auth = fields.DateTime()
    device = fields.Nested(DeviceSchemaOut)
