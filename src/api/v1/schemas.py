from db.extensions import ma
from db.models import HistoryAuth


class HistorySchemaOut(ma.SQLAlchemyAutoSchema):
    """Схема для возвращения истории авторизации пользователя."""
    class Meta:
        model = HistoryAuth
