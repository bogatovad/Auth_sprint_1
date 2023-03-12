from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request

from core.breaker import breaker, CustomCircuitBreakerError, handle_breaker_errors
from core.limiter import request_limit
from db.models import Permission, Role, User
from db.postgres import db

from ..schemas import ListRoleSchemaOut, RoleSchemaOut, UserSchemaOut
from .utils import return_error, set_permissions

role = Blueprint("role", __name__, url_prefix="/api/v1/role")


@request_limit
@breaker
@handle_breaker_errors
@role.post("/")
def add_role():
    """Метод для создания роли."""
    role_name = request.json['name']
    role = Role.query.filter_by(name=role_name).one_or_none()
    if role:
        return_error('role already exists', HTTPStatus.BAD_REQUEST)
    permissions_list = request.json['permissions']
    new_role = Role(name=role_name)
    set_permissions(db.session, Permission, new_role, permissions_list)
    db.session.add(new_role)
    db.session.commit()
    return RoleSchemaOut().dump(new_role), HTTPStatus.CREATED


@request_limit
@breaker
@handle_breaker_errors
@role.get("/")
def all_roles():
    """Метод для отображения всех ролей."""
    return [RoleSchemaOut().dump(role) for role in Role.query.all()], HTTPStatus.OK


@request_limit
@breaker
@handle_breaker_errors
@role.put("/<int:role_id>")
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
@breaker
@handle_breaker_errors
@role.delete("/<int:role_id>")
def remove_role(role_id: int):
    """Метод для удаления роли."""
    role_id = request.view_args["role_id"]
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify(message=f'Role {role_id} has been removed!'), HTTPStatus.OK



@request_limit
@breaker
@handle_breaker_errors
@role.post("/<int:role_id>/user/<user_id>")
def add_user_role(role_id: int, user_id: str):
    """Метод для добавления роли пользователю."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    user.add_role(role=role)
    db.session.commit()
    return UserSchemaOut().dump(user), HTTPStatus.OK



@request_limit
@breaker
@handle_breaker_errors
@role.delete("/<int:role_id>/user/<user_id>")
def revoke_user_role(role_id: int, user_id: str):
    """Метод для удаления роли у пользователя."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return make_response(UserSchemaOut().dump(user), HTTPStatus.OK)
    return jsonify(message=f'Role {role_id} doesnt set in this user.'), HTTPStatus.BAD_REQUEST


@request_limit
@breaker
@handle_breaker_errors
@role.get("/permissions/user/<user_id>")
def get_user_permissions(user_id):
    user = User.query.get_or_404(user_id)
    return ListRoleSchemaOut().dump({'roles': user.roles}), HTTPStatus.OK
