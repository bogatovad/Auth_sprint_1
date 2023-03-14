from __future__ import annotations

import datetime

from pydantic import BaseSettings, Field
import os

from core.enums import Providers


class AuthSettings(BaseSettings):
    db_name: str = Field("auth_database", env="POSTGRES_DB")
    pg_user: str = Field("app", env="POSTGRES_USER")
    pg_password: str = Field(env="POSTGRES_PASSWORD")
    db_host: str = Field("postgres_auth", env="POSTGRES_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    redis_host: str = Field("redis_auth", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    auth_port: int = Field(5000, env="AUTH_PORT")
    jwt_secret_key: str = Field("super-secret", env="JWT_SECRET_KEY")
    jaeger_host: str = Field("jaeger", env="JAEGER_HOST")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")
    tracer_enabled: bool = Field(False, env="TRACER_ENABLED")


    class Config:
        env_file = "envs/.env"


auth_config = AuthSettings()


class Config:
    DEBUG = True
    SECRET_KEY = "YOUR_RANDOM_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{auth_config.pg_user}:{auth_config.pg_password}@"
        f"{auth_config.db_host}/{auth_config.db_name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_HOST = 5000


config = Config()


CACHE_REFRESH_TOKEN_EXPIRATION_TIME = 15 * 60
CACHE_ACCESS_TOKEN_EXPERATION_TIME = 10 * 24 * 60 * 60
REFRESH_TOKEN_EXPIRATION_TIMEDELTA = datetime.timedelta(
    CACHE_REFRESH_TOKEN_EXPIRATION_TIME,
)
ACCESS_TOKEN_EXPERATION_TIMEDELTA = datetime.timedelta(
    CACHE_ACCESS_TOKEN_EXPERATION_TIME,
)


vk_config = {
    "name": Providers.VK.value,
    "client_id": os.environ.get('CLIENT_ID_VK'),
    "client_secret": os.environ.get('CLIENT_SECRET_VK'),
    "access_token_url": "https://oauth.vk.com/access_token",
    "access_token_params": {
        "client_id": os.environ.get('CLIENT_ID_VK'),
        "client_secret": os.environ.get('CLIENT_SECRET_VK'),
    },
    "authorize_url": "https://oauth.vk.com/authorize",
    "authorize_params": None,
    "api_base_url": "https://oauth.vk.com/",
    "client_kwargs": {"scope": "friends, notify, photos, wall, email"},
}

yandex_config = {
    "name": Providers.YANDEX.value,
    "client_id": os.environ.get('CLIENT_ID_YANDEX'),
    "client_secret": os.environ.get('CLIENT_SECRET_YANDEX'),
    "access_token_url": "https://oauth.yandex.ru/token",
    "access_token_params": None,
    "authorize_url": "https://oauth.yandex.ru/authorize",
    "authorize_params": None,
    "userinfo_endpoint": "https://login.yandex.ru/info?",
    "api_base_url": "https://oauth.yandex.ru/",
}


mail_config = {
    "name": Providers.MAIL.value,
    "client_id": os.environ.get('CLIENT_ID_MAIL'),
    "client_secret": os.environ.get('CLIENT_SECRET_MAIL'),
    "access_token_url": "https://oauth.mail.ru/token",
    "access_token_params": None,
    "authorize_url": "https://oauth.mail.ru/login",
    "authorize_params": None,
    "api_base_url": "https://oauth.mail.ru",
    "userinfo_endpoint": "https://oauth.mail.ru/userinfo"
}