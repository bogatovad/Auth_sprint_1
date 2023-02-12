from flask import Blueprint, jsonify, request

from db_models import Role
from ..schemas import RoleSchema
from db.extensions import db

role = Blueprint('role', __name__, url_prefix='/role')


@role.post('/')
def create_role():
    name = request.json['name']
    new_role = Role(name)

    db.session.add(new_role)
    db.session.commit()
    role_schema = RoleSchema()
    return role_schema.jsonify(new_role)


@role.get('/')
def get_roles():
    all_roles = Role.query.all()
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(all_roles)
    return jsonify(output.data)


@role.put('/')
def put_role():
    pass


@role.delete('/')
def delete_role():
    pass
