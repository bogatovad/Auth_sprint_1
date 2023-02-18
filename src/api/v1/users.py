from http import HTTPStatus

from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)

from db.redis_client import redis_client
from core.config import REFRESH_TOKEN_EXPIRATION_TIMEDELTA, ACCESS_TOKEN_EXPERATION_TIMEDELTA

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


class SignUp(Resource):
    def post(self):
        """
        Sign up.
        ---
        parameters:
          - in: body
            name: body
            required:
              - login
              - password
            schema:
              id: Credentials
              properties:
                login:
                  type: string
                password:
                  type: string
        responses:
          200:
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
        args = sign_up_parser.parse_args()
        login = args["login"]
        # TODO remove mock. Проверка наличия пользака в БД.
        #   Нужно вызвать метод класса (что-то вроде pg_connector.check_user) коннектора к постгре.
        user_exists = False
        if user_exists:
            return {"message": f"User '{login}' exists. Choose another login."}, HTTPStatus.CONFLICT
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
login_parser.add_argument("User-Agent", dest="agent", location="headers")


class Login(Resource):
    """Класс для логина пользователя.
    Параметры пользователя (логин, пароль, агент) находятся в args.
    Создаются access и refresh токены и возвращаются пользователю.
    """

    def post(self):
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
        args = login_parser.parse_args()
        # TODO remove mock. Проверка наличия пользака в БД.
        #   Нужно вызвать метод класса (что-то вроде pg_connector.check_user) коннектора к постгре.
        user = True
        user_id = 'user_id'  # TODO заменить на айди из базы
        identity = "something"  # TODO Remove mock, use user.id or something else
        access_token = create_access_token(identity, expires_delta=ACCESS_TOKEN_EXPERATION_TIMEDELTA)
        refresh_token = create_refresh_token(identity, expires_delta=REFRESH_TOKEN_EXPIRATION_TIMEDELTA)
        if not user:
            return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

        redis_client.set_user_refresh_token(user_id, refresh_token)
        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )


class Logout(Resource):
    """Выход пользователя из аккаунта."""

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
        jti = get_jwt()['jti']
        redis_client.set_user_invalid_access_token(user_id=user_id, jti=jti)
        return make_response(jsonify(message="Log outed"), HTTPStatus.OK)


class RefreshToken(Resource):
    """Обновление refresh токена."""

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
        identity = get_jwt_identity()  # TODO Remove mock, use user.id or something else
        refresh_token = create_refresh_token(identity, expires_delta=ACCESS_TOKEN_EXPERATION_TIMEDELTA)
        access_token = create_access_token(identity, expires_delta=ACCESS_TOKEN_EXPERATION_TIMEDELTA)
        redis_client.set_user_refresh_token(identity, refresh_token)
        return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )
