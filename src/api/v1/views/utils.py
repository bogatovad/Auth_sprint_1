from typing import Any
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from functools import wraps
from http import HTTPStatus
from werkzeug.exceptions import abort

from db.redis_client import redis_client
from db.models import User


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def set_permissions(session, model, role, permissions_list) -> None:
    for item in permissions_list:
        permission = get_or_create(
            session,
            model,
            resource=item['resource'],
            method=item['method'])
        role.add_permission(permission)


def return_error(text: Any | None, http_code: int):
    return abort(make_response(jsonify({'msg': text}), http_code))


def get_user_roles(user_id):
    user = User.query.get_or_404(user_id)
    return [role.name for role in user.roles]


def admin_only():
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            jti = get_jwt()["jti"]
            token_valid = redis_client.check_if_access_token_is_invalid(jti)
            if not token_valid:
                return_error('Invalid token', HTTPStatus.FORBIDDEN)
            user_id = get_jwt_identity()
            roles_list = get_user_roles(user_id)
            if not 'admin' in roles_list or 'superuser' in roles_list:
                return_error('Not enough permissions', HTTPStatus.FORBIDDEN)
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator