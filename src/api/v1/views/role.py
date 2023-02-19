from http import HTTPStatus

from flask import Blueprint, jsonify, request, make_response

from db_models import Role, User, Permission
from ..schemas import RoleSchema, UserSchema
from db.extensions import db
from .utils import get_or_create, update_permissions

role = Blueprint('role', __name__, url_prefix='/api/v1/role')


@role.post('/')
def add_role():
    role_name = request.json['name']
    permissions_list = request.json['permissions']
    new_role = Role(name=role_name)
    update_permissions(db.session, Permission, new_role, permissions_list)
    db.session.add(new_role)
    db.session.commit()
    role_schema = RoleSchema()
    return make_response(role_schema.jsonify(new_role), HTTPStatus.OK)
    

@role.get('/')
def all_roles():
    all_roles = Role.query.all()
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(all_roles)
    return make_response(jsonify(output), HTTPStatus.OK)


@role.put('/')
def update_role():
    role_id = request.json['id']
    role = Role.query.get_or_404(role_id)
    permissions_list = request.json['permissions']
    role.permissions = []
    update_permissions(db.session, Permission, role, permissions_list)
    db.session.commit()
    role_schema = RoleSchema()
    return make_response(role_schema.jsonify(role), HTTPStatus.OK)


@role.delete('/')
def remove_role():
    role_id = request.json['id']
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return make_response(HTTPStatus.NO_CONTENT)


@role.post('/<role_id>/user/<user_id>')
def add_user_role():
    role_id = request.view_args['role_id']
    role = Role.query.get_or_404(role_id)
    user_id = request.view_args['user_id']
    user = User.query.get_or_404(user_id)
    user.add_role(role=role)
    db.session.commit()
    user_schema = UserSchema()
    return make_response(user_schema.jsonify(user), HTTPStatus.OK)


@role.delete('/role_id>/user/<user_id>')
def revoke_user_role():
    role_id = request.view_args['role_id']
    role = Role.query.get_or_404(role_id)
    user_id = request.view_args['user_id']
    user = User.query.get_or_404(user_id)
    if role in user.role: 
        user.role.remove(role=role)
        db.session.commit()
        user_schema = UserSchema()
        return make_response(user_schema.jsonify(user), HTTPStatus.OK)
    return make_response(HTTPStatus.BAD_REQUEST)


@role.get('/permissions/user/<user_id>')
def get_user_permissions():
    user_id = request.view_args['user_id']
    user = User.query.get_or_404(user_id)
    return user.permissions_list
    