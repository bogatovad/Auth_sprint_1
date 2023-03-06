from datetime import datetime
from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_restful import Resource, request

from api.v1.arguments import (create_parser_args_change_auth_data,
                              create_parser_args_login,
                              create_parser_args_signup)
from api.v1.schemas import HistorySchemaOut
from db.redis_client import redis_client
from db.storage.device_storage import DeviceStorage
from db.storage.history_storage import HistoryAuthStorage
from db.storage.user_storage import PostgresUserStorage
from services.auth_service import JwtAuth
from services.exceptions import AuthError, DuplicateUserError
from flask import redirect
import requests
from db.models import User
from db.storage.social_account_storage import SocialAccountStorage

# Есть в authlib
class SocialServiceRedirect(Resource):
    """Метод для редиректа."""

    def get(self):
        client_id = '51567000'
        redirect_uri = 'http://127.0.0.1:5555/api/v1/auth/vk_logic'
        url_for_redirect = (
            f"https://oauth.vk.com/authorize?"
            f"client_id={client_id}"
            f"&display=page"
            f"&redirect_uri={redirect_uri}"
            f"&scope=friends,notify,photos,wall,email"
            f"&response_type=code"
            f"&v=5.131"
        )
        return redirect(url_for_redirect, code=302)


def generate_pass():
    import random

    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 11
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password


def signup(auth_service, login, email, user_agent):
    # делаем регистрацию пользователя если его нет.
    password = generate_pass()

    try:
        user = auth_service.signup(login, password, email)
    except DuplicateUserError as error:
        return {"message": error.message}, HTTPStatus.CONFLICT

    # сохранили устройство при регистрации пользователя
    # если в последующие разы вход будет осуществлен через другое устройство
    # то отсылаем уведомление.

    device_storage = DeviceStorage()
    device_storage.get_or_create(name=user_agent, owner=user)

    return user


def save_history_auth(user_agent, user_storage):
    history_storage = HistoryAuthStorage()
    device_storage = DeviceStorage()
    devices_user = list(device_storage.filter(name=user_agent, owner=user_storage))

    if not devices_user:
        # Отправить пользователю уведомление о том, что произошел вход с другого устройства.
        # Будет реализовано в следующем спринте.

        # сохраняем новое устройство пользователя.
        current_device = device_storage.create(name=user_agent, owner=user_storage)
    else:
        current_device = device_storage.get(name=user_agent, owner=user_storage)

    # делаем запись в таблицу history_auth.
    history_storage.create(
        user=user_storage, device=current_device, date_auth=datetime.now()
    )


def create_tokens(user):
    # Если пользователь тот, то выдаем токены.
    identity = str(user.id)
    refresh_token, access_token = create_refresh_token(identity), create_access_token(identity)

    # сохраняем refresh токен в редис.
    redis_client.set_user_refresh_token(identity, refresh_token)
    return refresh_token, access_token


class SocialService(Resource):
    def get(self):
        args = request.args
        code = args.get('code')
        client_secret = 'K56kDbZyl7dPFJxU4Evx'
        client_id = '51567000'
        redirect_uri = 'http://127.0.0.1:5555/api/v1/auth/vk_logic'
        access_token_url = (
            f"https://oauth.vk.com/access_token?"
            f"client_id={client_id}"
            f"&client_secret={client_secret}"
            f"&redirect_uri={redirect_uri}"
            f"&code={code}"
        )
        response = requests.get(access_token_url).json()
        access_token = response.get('access_token')
        user_id = response.get('user_id')
        email = response.get('email')

        user_agent = request.headers.get('User-Agent')
        user_storage = User.get_user_by_universal_login(email=email)
        auth_service = JwtAuth()
        social_account_storage = SocialAccountStorage()

        login = email

        # Если такого пользователя нет - регистрируем его.
        if user_storage is None:
            user = signup(auth_service, login, email, user_agent)

            # Далее нужно сделать запись в SocialService.
            social_account_storage.create(
                user=user,
                social_id=user_id,
                social_name='vk'
            )

            user_storage = user

        # Если пользователь есть, то проверим есть ли аккаунт связанный с таким social_id
        account = social_account_storage.get_account(social_id=str(user_id), social_name='vk')

        # Если найден аккаунт, то проверим тот ли пользователь привязан к нему
        if account.user == user_storage:

            refresh_token, access_token = create_tokens()
            save_history_auth(user_agent, user_storage)

            return make_response(
                jsonify(access_token=access_token, refresh_token=refresh_token),
                HTTPStatus.OK,
            )


class History(Resource):
    """Реализация метода для получения истории авторизаций."""
    @staticmethod
    def _parse_args():
        args = request.args
        per_page: int = 10
        if args:
            page = int(args["page"])
        else:
            page = 1
        return page, per_page

    @jwt_required()
    def get(self):
        page, per_page = self._parse_args()
        identity = get_jwt_identity()
        storage = PostgresUserStorage()
        history_storage = HistoryAuthStorage()
        user = storage.get_by_id(identity)
        history_queryset = history_storage.get_history_user(user.id)
        paginator = history_queryset.paginate(
            page=page, per_page=per_page, error_out=False
        )
        history = [HistorySchemaOut().dump(item) for item in paginator]
        return {user.login: history}


class ChangePersonalData(Resource):
    """Реализация метода по смене учетных данных."""

    @jwt_required()
    def post(self):
        args = create_parser_args_signup()
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

        return {"status": "Your personal data has been changed."}


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
        user_agent = args["user_agent"]

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
            jsonify(
                message=f"User '{login}' successfully created"), HTTPStatus.CREATED
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
        user_agent = args["user_agent"]

        auth_service = JwtAuth()

        try:
            user = auth_service.login(login, password)
        except AuthError as error:
            return {"message": error.message}, HTTPStatus.UNAUTHORIZED

        refresh_token, access_token = create_tokens()
        save_history_auth(user_agent, user)

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
