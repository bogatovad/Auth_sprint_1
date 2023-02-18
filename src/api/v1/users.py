from datetime import datetime
from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, jwt_required)
from flask_restful import Resource, reqparse

from db.base_user_storage import PostgresUserStorage
from db.crypto_pass import PBKDF2StoragePassword
from db.device_storage import DeviceStorage
from db.history_auth_storage import HistoryAuthStorage
from db.redis_client import redis_client

sign_up_parser = reqparse.RequestParser()
sign_up_parser.add_argument(
    "login",
    dest="login",
    location="form",
    required=True,
    type=str,
    help="Login required",
)
sign_up_parser.add_argument(
    "password",
    dest="password",
    type=str,
    location="form",
    required=True,
    help="Password required",
)
sign_up_parser.add_argument(
    "email",
    dest="email",
    type=str,
    location="form",
    required=True,
    help="Email required",
)
sign_up_parser.add_argument("last_name", dest="last_name", location="form", required=False, type=str)
sign_up_parser.add_argument("first_name", dest="first_name", location="form", required=False, type=str)
sign_up_parser.add_argument("User-Agent", dest="user_agent", location="headers")


class SignUp(Resource):
    def post(self):
        """Метод регистрации пользователя."""
        args = sign_up_parser.parse_args()

        login = args["login"]
        password = args["password"]
        email = args["email"]

        storage = PostgresUserStorage()
        password_checker = PBKDF2StoragePassword()

        if storage.exists(login):
            return {"message": f"User '{login}' exists. Choose another login."}, HTTPStatus.CONFLICT

        user = storage.create(
            login=login,
            password=password_checker.create_hash(password),
            email=email
        )

        # сохранили устройство при регистрации пользователя
        # если в последующие разы вход будет осуществлен через другое устройство
        # то отсылаем уведомление.

        device_storage = DeviceStorage()
        user_agent = args['user_agent']
        device_storage.create(name=user_agent, owner=user)

        return make_response(jsonify(message=f"User '{login}' successfully created"), HTTPStatus.OK)


login_parser = reqparse.RequestParser()
login_parser.add_argument(
    "login",
    dest="login",
    location="form",
    required=True,
    type=str,
    help="Login required",
)
login_parser.add_argument(
    "password",
    dest="password",
    type=str,
    location="form",
    required=True,
    help="Password required",
)
login_parser.add_argument("User-Agent", dest="user_agent", location="headers")


class Login(Resource):
    """
    Класс для логина пользователя.
    Параметры пользователя (логин, пароль, агент) находятся в args.
    Создаются access и refresh токены и возвращаются пользователю.
    """

    def post(self):
        args = login_parser.parse_args()

        login = args["login"]
        user_agent = args['user_agent']

        storage = PostgresUserStorage()

        if not storage.exists(login):
            return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

        user = storage.get(login=login)
        identity = user.id
        access_token, refresh_token = create_refresh_token(identity), create_access_token(identity)

        history_storage = HistoryAuthStorage()
        device_storage = DeviceStorage()
        devices_user = list(device_storage.filter(name=user_agent, owner=user))

        if not devices_user:
            # Отправить пользователю уведомление о том, что произошел вход с другого устройства.
            # ...

            # сохраняем новое устройство пользователя.
            current_device = device_storage.create(name=user_agent, owner=user)
        else:
            current_device = device_storage.get(name=user_agent, owner=user)

        # делаем запись в таблицу history_auth.
        history_storage.create(user=user, device=current_device, date_auth=datetime.now())

        # сохраняем refresh токен в редис.
        redis_client.set_user_refresh_token(user.id, refresh_token)

        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )


class Logout(Resource):
    """Выход пользователя из аккаунта."""

    @jwt_required(refresh=True)
    def post(self):
        jwt = get_jwt()
        # TODO реализовать redis_client.put_invalid_token(jwt)
        return make_response(jsonify(message="Log outed"), HTTPStatus.OK)


class RefreshToken(Resource):
    """Обновление refresh токена."""

    @jwt_required(refresh=True)
    def get(self):
        identity = "something"  # TODO Remove mock, use user.id or something else
        access_token, refresh_token = create_refresh_token(identity), create_access_token(identity)
        old_jwt = get_jwt()
        # TODO реализовать redis_client.refresh_user_token(user_id, old_jwt, access_token)
        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )
