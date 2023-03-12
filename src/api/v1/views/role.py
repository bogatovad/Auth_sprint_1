from __future__ import annotations

from http import HTTPStatus
from flask import Blueprint, jsonify, make_response, request

from core.limiter import request_limit
from db.models import Permission, Role, User
from db.postgres import db
from db.redis_client import redis_client
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from ..schemas import ListRoleSchemaOut, RoleSchemaOut, UserSchemaOut
from .utils import return_error, set_permissions, admin_only, get_user_roles

role = Blueprint("role", __name__, url_prefix="/api/v1/role")


@request_limit
@role.post("/")
@admin_only()
def add_role():
    """Метод для создания роли."""
    role_name = request.json["name"]
    role = Role.query.filter_by(name=role_name).one_or_none()
    if role:
        return_error("role already exists", HTTPStatus.BAD_REQUEST)
    permissions_list = request.json["permissions"]
    new_role = Role(name=role_name)
    set_permissions(db.session, Permission, new_role, permissions_list)
    db.session.add(new_role)
    db.session.commit()
    return RoleSchemaOut().dump(new_role), HTTPStatus.CREATED


@request_limit
@role.get("/")
@admin_only()
def all_roles():
    """Метод для отображения всех ролей."""
    return [RoleSchemaOut().dump(role) for role in Role.query.all()], HTTPStatus.OK


@request_limit
@role.put("/<int:role_id>")
@admin_only()
def update_role(role_id: int):
    """Метод для обновления роли."""
    role = Role.query.get_or_404(role_id)
    role_name = request.json["name"]
    permissions_list = request.json["permissions"]
    role.permissions = []
    role.name = role_name
    set_permissions(db.session, Permission, role, permissions_list)
    db.session.commit()
    return RoleSchemaOut().dump(role), HTTPStatus.OK


@request_limit
@role.delete("/<int:role_id>")
@admin_only()
def remove_role(role_id: int):
    """Метод для удаления роли."""
    role_id = request.view_args["role_id"]
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify(message=f"Role {role_id} has been removed!"), HTTPStatus.OK


@request_limit
@role.post("/<int:role_id>/user/<user_id>")
@admin_only()
def add_user_role(role_id: int, user_id: str):
    """Метод для добавления роли пользователю."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    user.add_role(role=role)
    db.session.commit()
    return UserSchemaOut().dump(user), HTTPStatus.OK


@request_limit
@role.delete("/<int:role_id>/user/<user_id>")
@admin_only()
def revoke_user_role(role_id: int, user_id: str):
    """Метод для удаления роли у пользователя."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return make_response(UserSchemaOut().dump(user), HTTPStatus.OK)
    return (
        jsonify(message=f"Role {role_id} doesnt set in this user."),
        HTTPStatus.BAD_REQUEST,
    )


@request_limit
@role.get("/permissions/user/<user_id>")
@admin_only()
def get_user_permissions(user_id):
    user = User.query.get_or_404(user_id)
    return ListRoleSchemaOut().dump({"roles": user.roles}), HTTPStatus.OK


@request_limit
@role.get("/user/roles")
@jwt_required()
def get_user_roles():
    jti = get_jwt()["jti"]
    token_valid = redis_client.check_if_access_token_is_invalid(jti)
    if not token_valid:
        return_error('Invalid token', HTTPStatus.FORBIDDEN)
    user_id = get_jwt_identity()
    roles_list = get_user_roles(user_id)
    return roles_list, HTTPStatus.OK