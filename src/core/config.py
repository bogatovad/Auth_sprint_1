import datetime
import os

from pydantic import BaseSettings, Field


class AuthSettings(BaseSettings):
    db_name: str = Field('auth_database', env='DB_NAME')
    pg_user: str = Field('app', env='POSTGRES_USER')
    pg_password: str = Field('qwerty123', env='POSTGRES_PASSWORD') #check envs
    db_host: str = Field('postgres', env='POSTGRES_HOST')
    db_port: int = Field(5432, env='DB_PORT')
    redis_host: str = Field('redis_auth', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    auth_port: int = Field(5000, env='AUTH_PORT')

    class Config:
          env_file = ".env"


auth_config = AuthSettings()


class Config(object):
    DEBUG = True

    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{auth_config.pg_user}:{auth_config.pg_password}@{auth_config.db_host}/{auth_config.db_name}'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

CACHE_REFRESH_TOKEN_EXPIRATION_TIME = 15 * 60
CACHE_ACCESS_TOKEN_EXPERATION_TIME = 10 * 24 * 60 * 60
REFRESH_TOKEN_EXPIRATION_TIMEDELTA = datetime.timedelta(
    CACHE_REFRESH_TOKEN_EXPIRATION_TIME
)
ACCESS_TOKEN_EXPERATION_TIMEDELTA = datetime.timedelta(
    CACHE_ACCESS_TOKEN_EXPERATION_TIME
)

config = Config()
