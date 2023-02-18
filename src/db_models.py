import uuid
from sqlalchemy import Table, Column, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db
from db.extensions import metadata


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    roles = db.relationship(
        'Role',
        secondary='related_roles',
        lazy='subquery',
        backref=db.backref("users", lazy=True),
    )
    history_auth_id = db.Column(db.Integer, db.ForeignKey('history_auth.id'), nullable=True)

    def __repr__(self):
        return f'<User {self.login}>'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'


class Device(db.Model):
    """Модель, описывающая устройство пользователя user."""

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)

    # Через устройство мы можем получить историю авторизаций.
    history = db.relationship("HistoryAuth", backref='device', lazy=True)


class HistoryAuth(db.Model):
    """Модель, описывающая факт авторизаци пользователем
    user с устройства device в дату date_auth."""

    __tablename__ = 'history_auth'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    # С каждой авторизацией связан пользователь.
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    date_auth = db.Column(db.DateTime, index=True)

    # С каждой авторизацией связано устройство с которого она была выполнена.
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)


related_roles = Table(
    'related_roles',
    metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
)
