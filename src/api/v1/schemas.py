from marshmallow import Schema, fields


class DeviceSchemaOut(Schema):
    """Схема для возвращения устройства пользователя."""

    name = fields.String()


class HistorySchemaOut(Schema):
    """Схема для возвращения истории авторизации пользователя."""

    date_auth = fields.DateTime()
    device = fields.Nested(DeviceSchemaOut)

