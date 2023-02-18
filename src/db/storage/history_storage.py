from datetime import datetime

from db.models import Device, HistoryAuth, User
from db.postgres import db


class HistoryAuthStorage:
    @staticmethod
    def create(user: User, device: Device, date_auth: datetime) -> HistoryAuth:
        history_auth = HistoryAuth(user=user, device=device, date_auth=date_auth)
        db.session.add(history_auth)
        db.session.commit()
        return history_auth
