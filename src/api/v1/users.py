from datetime import datetime
from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from flask_restful import Resource

from db.redis_client import redis_client
from api.v1.schemas import HistorySchemaOut
from db.storage.device_storage import DeviceStorage
from db.storage.history_storage import HistoryAuthStorage

from api.v1.arguments import (
    create_parser_args_signup,
    create_parser_args_login,
    create_parser_args_change_auth_data
)
from db.storage.user_storage import PostgresUserStorage
from services.auth_service import JwtAuth
from services.exceptions import AuthError, DuplicateUserError


class History(Resource):
    """Реализация метода для получения истории авторизаций."""

    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        storage = PostgresUserStorage()
        user = storage.get_by_id(identity)
        history = [HistorySchemaOut().dump(item) for item in user.history]
        return {user.login: history}


class ChangePersonalData(Resource):
    """Реализация метода по смене учетных данных."""

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        storage = PostgresUserStorage()
        user = storage.get_by_id(identity)
        args = create_parser_args_change_auth_data()
        login = args["login"]
        password = args["password"]

        if login is not None:
            user.login = login
        if password is not None:
            user.password = password

        return {'status': 'Your personal data has been changed.'}


class SignUp(Resource):
    """Реализация метода signup."""

    @staticmethod
    def post():
        """
        Sign up.
        ---
        parameters:
          - in: body
            name: body
            required:
              - login
              - password
              - email
            schema:
              id: Credentials
              properties:
                login:
                  type: string
                password:
                  type: string
                email:
                  type: string
        responses:
          201:
            description: User created
            schema:
              message:
              example: User '{login}' successfully created
          409:
            description: User exists
            schema:
              message:
                type: string
                example: User '{login}' exists. Choose another login.
        """
        args = create_parser_args_signup()
        login = args["login"]
        password = args["password"]
        email = args["email"]
        user_agent = args['user_agent']

        auth_service = JwtAuth()

        try:
            user = auth_service.signup(login, password, email)
        except DuplicateUserError as error:
            return {"message": error.message}, HTTPStatus.CONFLICT

        # сохранили устройство при регистрации пользователя
        # если в последующие разы вход будет осуществлен через другое устройство
        # то отсылаем уведомление.

        device_storage = DeviceStorage()
        device_storage.get_or_create(name=user_agent, owner=user)
        return make_response(
            jsonify(message=f"User '{login}' successfully created"), HTTPStatus.CREATED
        )


class Login(Resource):
    """Реализация метода login.
    Параметры пользователя (логин, пароль, агент) находятся в args.
    Создаются access и refresh токены и возвращаются пользователю.
    """
    @staticmethod
    def post():
        """
        Login
        ---
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Credentials'
        responses:
          200:
            description:
            schema:
              $ref: '#/definitions/TokensPair'
          403:
            description: Unauthorized
            schema:
              message:
                type: string
                example: Unauthorized
        """
        args = create_parser_args_login()

        login = args["login"]
        password = args["password"]
        user_agent = args['user_agent']

        auth_service = JwtAuth()

        try:
            user = auth_service.login(login, password)
        except AuthError as error:
            return {"message": error.message}, HTTPStatus.UNAUTHORIZED

        identity = str(user.id)
        refresh_token, access_token = create_refresh_token(identity), create_access_token(identity)

        history_storage = HistoryAuthStorage()
        device_storage = DeviceStorage()
        devices_user = list(device_storage.filter(name=user_agent, owner=user))

        if not devices_user:
            # Отправить пользователю уведомление о том, что произошел вход с другого устройства.
            # Будет реализовано в следующем спринте.

            # сохраняем новое устройство пользователя.
            current_device = device_storage.create(name=user_agent, owner=user)
        else:
            current_device = device_storage.get(name=user_agent, owner=user)

        # делаем запись в таблицу history_auth.
        history_storage.create(user=user, device=current_device, date_auth=datetime.now())

        # сохраняем refresh токен в редис.
        redis_client.set_user_refresh_token(identity, refresh_token)

        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )


class Logout(Resource):
    """Реализация метода logout."""

    @jwt_required()
    def post(self):
        """
        Logout.
        ---
        description: Send access_token in authorization.
        responses:
          200:
            description: Success
            schema:
              properties:
                message:
                  type: string
                  example: Log outed

        """
        user_id = get_jwt_identity()
        jti = get_jwt()["jti"]
        redis_client.set_user_invalid_access_token(user_id=user_id, jti=jti)
        return make_response(jsonify(message="Log outed"), HTTPStatus.OK)


class RefreshToken(Resource):
    """Реализация метода refresh."""

    @jwt_required(refresh=True)
    def get(self):
        """
        Refreshing tokens.
        ---
        description: Send refresh_token in authorization.
        responses:
          200:
            description: A new pair of access and refresh tokens
            schema:
              id: TokensPair
              properties:
                access_token:
                  type: string
                  description: Access_token
                refresh_token:
                  type: string
                  description: Refresh_token
        """
        identity = get_jwt_identity()
        refresh_token = create_refresh_token(identity)
        access_token = create_access_token(identity)
        redis_client.set_user_refresh_token(identity, refresh_token)
        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )
