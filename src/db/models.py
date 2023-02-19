import uuid
from sqlalchemy.dialects.postgresql import UUID
from .postgres import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    history_auth_id = db.Column(
        db.Integer, db.ForeignKey("history_auth.id"), nullable=True
    )

    def __repr__(self):
        return f"<User {self.login}>"


class Device(db.Model):
    """Таблица, описывающая устройство пользователя."""

    __tablename__ = "history_auth"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey("history_auth.id"), nullable=True)


class HistoryAuth(db.Model):
    """Таблица, описывающая история авторизаций."""

    __tablename__ = "history_auth"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user = db.relationship(User, backref="history", lazy=True)
    device = db.relationship(Device, lazy=True)
    date_auth = db.Column(db.Date, index=True)
