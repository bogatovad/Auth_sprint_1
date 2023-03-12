from __future__ import annotations

from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth_client = OAuth()

oauth_client.register(
    name="vk",
    client_id="51567000",
    client_secret="K56kDbZyl7dPFJxU4Evx",
    access_token_url="https://oauth.vk.com/access_token",
    access_token_params={
        "client_id": "51567000",
        "client_secret": "K56kDbZyl7dPFJxU4Evx",
    },
    authorize_url="https://oauth.vk.com/authorize",
    authorize_params=None,
    api_base_url="https://oauth.vk.com/",
    client_kwargs={"scope": "friends, notify, photos, wall, email"},
)

oauth_client.register(
    name="yandex",
    client_id="8fc229d7c9cc4517897549ed19f82964",
    client_secret="c708f75b1c764f70a0a91c78b69b2831",
    access_token_url="https://oauth.yandex.ru/token",
    access_token_params=None,
    authorize_url="https://oauth.yandex.ru/authorize",
    authorize_params=None,
    userinfo_endpoint="https://login.yandex.ru/info?",
    api_base_url="https://oauth.yandex.ru/",
)

oauth_client.register(
    name="mail",
    client_id="66c3117357a14117a98d126d6d74777b",
    client_secret="9f26b8a1294f4ff9a49504632af387d3",
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
