from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request

from core.breaker import breaker, CustomCircuitBreakerError
from core.limiter import request_limit
from db.models import Permission, Role, User
from db.postgres import db

from ..schemas import ListRoleSchemaOut, RoleSchemaOut, UserSchemaOut
from .utils import return_error, set_permissions

role = Blueprint("role", __name__, url_prefix="/api/v1/role")


@request_limit
@breaker
@role.post("/")
def add_role():
    """Метод для создания роли."""
    try:
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
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.get("/")
def all_roles():
    """Метод для отображения всех ролей."""
    try:
        return [RoleSchemaOut().dump(role) for role in Role.query.all()], HTTPStatus.OK
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.put("/<int:role_id>")
def update_role(role_id: int):
    """Метод для обновления роли."""
    try:
        role = Role.query.get_or_404(role_id)
        role_name = request.json["name"]
        permissions_list = request.json["permissions"]
        role.permissions = []
        role.name = role_name
        set_permissions(db.session, Permission, role, permissions_list)
        db.session.commit()
        return RoleSchemaOut().dump(role), HTTPStatus.OK
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.delete("/<int:role_id>")
def remove_role(role_id: int):
    """Метод для удаления роли."""
    try:
        role_id = request.view_args["role_id"]
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return jsonify(message=f'Role {role_id} has been removed!'), HTTPStatus.OK
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.post("/<int:role_id>/user/<user_id>")
def add_user_role(role_id: int, user_id: str):
    """Метод для добавления роли пользователю."""
    try:
        role = Role.query.get_or_404(role_id)
        user = User.query.get_or_404(user_id)
        user.add_role(role=role)
        db.session.commit()
        return UserSchemaOut().dump(user), HTTPStatus.OK
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.delete("/<int:role_id>/user/<user_id>")
def revoke_user_role(role_id: int, user_id: str):
    """Метод для удаления роли у пользователя."""
    try:
        role = Role.query.get_or_404(role_id)
        user = User.query.get_or_404(user_id)
        if role in user.roles:
            user.roles.remove(role)
            db.session.commit()
            return make_response(UserSchemaOut().dump(user), HTTPStatus.OK)
        return jsonify(message=f'Role {role_id} doesnt set in this user.'), HTTPStatus.BAD_REQUEST
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE


@request_limit
@breaker
@role.get("/permissions/user/<user_id>")
def get_user_permissions(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return ListRoleSchemaOut().dump({'roles': user.roles}), HTTPStatus.OK
    except CustomCircuitBreakerError as e:
        return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE
