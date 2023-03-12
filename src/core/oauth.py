from __future__ import annotations

from authlib.integrations.flask_client import OAuth
from flask import Flask
import os

oauth_client = OAuth()


oauth_client.register(
    name="vk",
    client_id=os.environ.get('CLIENT_ID_VK'),
    client_secret=os.environ.get('CLIENT_SECRET_VK'),
    access_token_url="https://oauth.vk.com/access_token",
    access_token_params={
        "client_id": os.environ.get('CLIENT_ID_VK'),
        "client_secret": os.environ.get('CLIENT_SECRET_VK'),
    },
    authorize_url="https://oauth.vk.com/authorize",
    authorize_params=None,
    api_base_url="https://oauth.vk.com/",
    client_kwargs={"scope": "friends, notify, photos, wall, email"},
)

oauth_client.register(
    name="yandex",
    client_id=os.environ.get('CLIENT_ID_YANDEX'),
    client_secret=os.environ.get('CLIENT_SECRET_YANDEX'),
    access_token_url="https://oauth.yandex.ru/token",
    access_token_params=None,
    authorize_url="https://oauth.yandex.ru/authorize",
    authorize_params=None,
    userinfo_endpoint="https://login.yandex.ru/info?",
    api_base_url="https://oauth.yandex.ru/",
)

oauth_client.register(
    name="mail",
    client_id=os.environ.get('CLIENT_ID_MAIL'),
    client_secret=os.environ.get('CLIENT_SECRET_MAIL'),
    access_token_url="https://oauth.mail.ru/token",
    access_token_params=None,
    authorize_url="https://oauth.mail.ru/login",
    authorize_params=None,
    api_base_url="https://oauth.mail.ru",
    userinfo_endpoint="https://oauth.mail.ru/userinfo",
)


def init_oauth(app: Flask):
    oauth_client.init_app(app)


def get_client():
    return oauth_client
