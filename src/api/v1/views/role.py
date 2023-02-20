from http import HTTPStatus

from flask import Blueprint, make_response, request, jsonify

from db.postgres import db
from db.models import Permission, Role, User

from ..schemas import RoleSchemaOut, UserSchemaOut, ListRoleSchemaOut
from .utils import update_permissions

role = Blueprint('role', __name__, url_prefix='/api/v1/role')


@role.post('/')
def add_role():
    """Метод для создания роли."""
    role_name = request.json['name']
    permissions_list = request.json['permissions']
    new_role = Role(name=role_name)
    update_permissions(db.session, Permission, new_role, permissions_list)
    db.session.add(new_role)
    db.session.commit()
    return make_response(RoleSchemaOut().dump(new_role), HTTPStatus.OK)


@role.get('/')
def all_roles():
    """Метод для отображения всех ролей."""
    return make_response(
        [RoleSchemaOut().dump(role) for role in Role.query.all()], HTTPStatus.OK
    )


@role.put('/<int:role_id>')
def update_role(role_id: int):
    """Метод для обновления роли."""
    role = Role.query.get_or_404(role_id)
    role_name = request.json['name']
    permissions_list = request.json['permissions']
    role.permissions = []
    role.name = role_name
    update_permissions(db.session, Permission, role, permissions_list)
    db.session.commit()
    return make_response(RoleSchemaOut().dump(role), HTTPStatus.OK)


@role.delete('/<int:role_id>')
def remove_role(role_id: int):
    """Метод для удаления роли."""
    role_id = request.view_args['role_id']
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return make_response(jsonify(message=f'Role {role_id} has been removed!'), HTTPStatus.OK)


@role.post('/<int:role_id>/user/<user_id>')
def add_user_role(role_id: int, user_id: str):
    """Метод для добавления роли пользователю."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    user.add_role(role=role)
    db.session.commit()
    return make_response(UserSchemaOut().dump(user), HTTPStatus.OK)


@role.delete('/<int:role_id>/user/<user_id>')
def revoke_user_role(role_id: int, user_id: str):
    """Метод для удаления роли у пользователя."""
    role = Role.query.get_or_404(role_id)
    user = User.query.get_or_404(user_id)
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return make_response(UserSchemaOut().dump(user), HTTPStatus.OK)
    return make_response(jsonify(message=f'Role {role_id} doesnt set in this user.'), HTTPStatus.BAD_REQUEST)


@role.get('/permissions/user/<user_id>')
def get_user_permissions(user_id):
    user = User.query.get_or_404(user_id)
    return make_response(ListRoleSchemaOut().dump({'roles': user.roles}), HTTPStatus.OK)
