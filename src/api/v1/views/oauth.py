from __future__ import annotations

from http import HTTPStatus

from api.v1.users import create_tokens
from api.v1.users import save_history_auth
from core.oauth import get_client
from db.models import User
from db.storage.device_storage import DeviceStorage
from db.storage.social_account_storage import SocialAccountStorage
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from flask import url_for
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from services.auth_service import JwtAuth
from services.oauth_service import OAuthService, get_provider

oauth = Blueprint("oauth", __name__, url_prefix="/api/v1/oauth")


def generate_pass():
    import random

    chars = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    length = 11
    password = ""
    for _ in range(length):
        password += random.choice(chars)
    return password


def signup(auth_service: OAuthService, login: str, email: str, user_agent: str) -> User:
    # делаем регистрацию пользователя если его нет.
    password = generate_pass()
    user = auth_service.signup(login, password, email)

    # сохранили устройство при регистрации пользователя
    # если в последующие разы вход будет осуществлен через другое устройство
    # то отсылаем уведомление.

    device_storage = DeviceStorage()
    device_storage.get_or_create(name=user_agent, owner=user)
    return user


def get_or_create(auth_service: OAuthService, login: str, email: str, user_agent: str) -> User:
    try:
        user = signup(auth_service, login, email, user_agent)
    except Exception as ex:
        user = User.get_user_by_universal_login(login=login, email=email)
    return user


@oauth.get("/login/<string:provider_name>")
def login(provider_name: str):
    client = get_client().create_client(provider_name)
    redirect_uri = url_for(
        f"oauth.authorize",
        _external=True,
        provider_name=provider_name,
    )
    return client.authorize_redirect(redirect_uri)


@oauth.get("/authorize/<string:provider_name>")
def authorize(provider_name: str):
    oauth_service: OAuthService = get_provider(provider_name)
    user_info = oauth_service.get_user_info()
    user_agent = request.headers.get("user_agent")
    user_storage = User.get_user_by_universal_login(email=user_info.email)
    auth_service = JwtAuth()
    social_account_storage = SocialAccountStorage()
    login = user_info.email

    # Проверим есть ли аккаунт связанный с таким social_id и provider_name
    account = social_account_storage.get_account(
        social_id=str(user_info.id),
        social_name=provider_name,
    )

    # Если такого пользователя нет или аккаунт не найден - регистрируем его.
    if user_storage is None or account is None:
        user = get_or_create(auth_service, login, user_info.email, user_agent)

        # Далее нужно сделать запись в SocialService.
        account = social_account_storage.create(
            user=user,
            social_id=user_info.id,
            social_name=provider_name,
        )

        user_storage = user

    # Если найден аккаунт, то проверим тот ли пользователь привязан к нему
    if account.user == user_storage:
        identity = str(user_storage.id)
        refresh_token, access_token = create_tokens(identity)
        save_history_auth(user_agent, user_storage)

    return make_response(
        jsonify(access_token=access_token, refresh_token=refresh_token),
        HTTPStatus.OK,
    )


@oauth.delete("remove/<string:provider_name>")
@jwt_required()
def remove(provider_name: str):
    user_id = get_jwt_identity()
    oauth_service = get_provider(provider_name)
    oauth_service.remove(user_id)
    return jsonify(message=f"Accont {provider_name} has been removed!"), HTTPStatus.OK
