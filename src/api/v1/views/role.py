from flask import Blueprint
from flask_marshmallow import Marshmallow


role = Blueprint('role', __name__, url_prefix='/role')


@role.post('/')
def create_role():
    pass


@role.get('/')
def get_roles():
    pass


@role.put('/')
def put_role():
    pass


@role.delete('/')
def delete_role():
    pass
