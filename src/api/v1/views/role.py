from http import HTTPStatus

from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from flask_restful import Resource

from db_models import Role
from ..schemas import RoleSchema
from db.extensions import db

role = Blueprint('role', __name__, url_prefix='/api/v1/role')


"""class RoleApi(Resource):

    def get(self):
        all_roles = Role.query.all()
        role_schema = RoleSchema(many=True)
        output = role_schema.dump(all_roles)
        return make_response(jsonify(output), HTTPStatus.OK)"""


@role.post('/post')
def add_role():
    name = request.json.get['name']
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
    return jsonify(output)


@role.put('/')
def put_role():
    pass


@role.delete('/')
def remove_role():
    db_role = _get_role(role_name, check_missing=True)
    db.session.delete(db_role)
    db.session.commit()
