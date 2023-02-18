import uuid

from sqlalchemy.dialects.postgresql import UUID

from .postgres import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)

    # храним хэш пароля - бинарные данные.
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    devices = db.relationship("Device", backref='owner', lazy=True)
    history = db.relationship("HistoryAuth", backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.login}>'


class Device(db.Model):
    """Таблица, описывающая устройство пользователя user."""

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)

    history = db.relationship("HistoryAuth", backref='device', uselist=False, lazy=True)


class HistoryAuth(db.Model):
    """Таблица, описывающая факт авторизаци пользователем
    user с устройства device в дату date_auth."""

    __tablename__ = 'history_auth'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)

    # todo: проверить что создается поле именно со временем.
    date_auth = db.Column(db.DateTime, index=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

