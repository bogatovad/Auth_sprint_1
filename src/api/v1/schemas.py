from __future__ import annotations

from marshmallow import fields
from marshmallow import Schema


class PermissionSchemaOut(Schema):
    """Схема для возвращения устройства доступа."""

    resource = fields.String()
    method = fields.String()


class RoleSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    name = fields.String()
    permissions = fields.Nested(PermissionSchemaOut, many=True)


class ListRoleSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    roles = fields.Nested(RoleSchemaOut, many=True)


class DeviceSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    name = fields.String()


class HistorySchemaOut(Schema):
    """Схема для возвращения истории авторизации пользователя."""

    date_auth = fields.DateTime()
    device = fields.Nested(DeviceSchemaOut)


class UserSchemaOut(Schema):
    """Схема для возвращения пользовтеля."""

    login = fields.String()
    roles = fields.Nested(RoleSchemaOut, many=True)
