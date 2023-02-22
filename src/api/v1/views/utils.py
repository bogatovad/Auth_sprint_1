from typing import Any

from flask import jsonify, make_response
from werkzeug.exceptions import abort


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def set_permissions(session, model, role, permissions_list):
    for item in permissions_list:
        permission = get_or_create(
            session,
            model,
            resource=item['resource'],
            method=item['method'])
        role.add_permission(permission)


def return_error(text: Any | None, http_code: int):
    return abort(make_response(jsonify({'msg': text}), http_code))
