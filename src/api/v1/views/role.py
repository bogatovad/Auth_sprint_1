from http import HTTPStatus

from flask import Blueprint, jsonify, request, make_response
from flask_restful import Resource

from db_models import Role
from ..schemas import RoleSchema
from db.extensions import db

role = Blueprint('role', __name__, url_prefix='/api/v1/role')


@role.post('/')
def add_role():
    role_name = request.args['name']
    new_role = Role(name=role_name)

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
    id = request.args['id']
    db_role = Role.query.get(id)

    role_name = request.args['name']
    db_role.name = role_name
    db.session.commit()
    role_schema = RoleSchema()
    return make_response(role_schema.jsonify(db_role), HTTPStatus.OK)


@role.delete('/')
def remove_role():
    id = request.args['id']
    db_role = Role.query.get(id)
    db.session.delete(db_role)
    db.session.commit()
    return make_response('Successfully deleted', HTTPStatus.NO_CONTENT)  
    
