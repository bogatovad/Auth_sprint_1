import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db


class User(db.Model):
    """Модель, описывающая пользователя."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)

    # Храним хэш пароля - бинарные данные.
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    # C пользователем связаны его устройства.
    devices = db.relationship("Device", backref="owner", lazy=True)

    # C пользователем связана его история.
    history = db.relationship("HistoryAuth", backref="user", lazy=True)

    # C пользователем связаны его роли.
    roles = db.relationship("Role", secondary="users_roles")

    def __repr__(self):
        return f"<User {self.login}>"

    def add_role(self, role):
        self.roles.append(role)


class Device(db.Model):
    """Модель, описывающая устройство пользователя user."""

    __tablename__ = "device"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)

    # Через устройство мы можем получить историю авторизаций.
    history = db.relationship("HistoryAuth", backref="device", lazy=True)


class HistoryAuth(db.Model):
    """Модель, описывающая факт авторизаци пользователем
    user с устройства device в дату date_auth."""

    __tablename__ = "history_auth"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    # С каждой авторизацией связан пользователь.
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    date_auth = db.Column(db.DateTime)

    # С каждой авторизацией связано устройство с которого она была выполнена.
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)


class Permission(db.Model):
    """Модель, описывающая доступ к ресурсу."""

    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    # доступ описывается ресурсом и методом.
    resource = db.Column(db.String, nullable=False)
    method = db.Column(db.String, nullable=False)

    roles = db.relationship("Role", secondary="permissions_roles")


class PermissionsRole(db.Model):
    """Промежуточная модель-связка для Role и Permissions."""

    __tablename__ = "permissions_roles"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"))


class UserRole(db.Model):
    """Промежуточная модель-связка для Role и Permissions."""

    __tablename__ = "users_roles"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))


class Role(db.Model):
    """Модель, описывающая роль."""

    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    # Набор прав (доступов), которые содержит данная роль.
    permissions = db.relationship("Permission", secondary="permissions_roles")

    users = db.relationship("User", secondary="users_roles")

    def add_permission(self, permission):
        self.permissions.append(permission)
