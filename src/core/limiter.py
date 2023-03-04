from datetime import datetime
from http import HTTPStatus

from db.redis_client import redis_client
from flask import abort, jsonify, make_response, request

REQUEST_LIMIT_PER_MINUTE = 20


def request_limit(func):
    def wrapper(*args, **kwargs):
        pipe = redis_client.db_for_request_limit.pipeline()
        now = datetime.now()
        key = f'{request.headers.get("Authorization")}:{now.minute}'
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > REQUEST_LIMIT_PER_MINUTE:
            abort(make_response(jsonify(message="too many requests"), HTTPStatus.TOO_MANY_REQUESTS))
        return func(*args, **kwargs)

    return wrapper