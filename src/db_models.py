import uuid
from sqlalchemy import Table, Column, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db
from db.extensions import metadata


#related_roles = Table(
#    'related_roles',
#    metadata,
#    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
#    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
#)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    roles = db.relationship(
        "Role",
        secondary="roles_users",
        backref=db.backref("users", lazy="dynamic"),
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


class RolesUsers(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id"))
    role_id = db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"))