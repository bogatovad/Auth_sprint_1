import os
from pydantic import BaseSettings, Field

class AuthSettings(BaseSettings):
    db_name: str = Field('postgres', env='DB_NAME')
    pg_user: str = Field('auth', env='POSTGRES_USER')
    pg_password: str = Field('auth', env='POSTGRES_PASSWORD')
    db_host: str = Field('postgres_auth', env='POSTGRES_HOST')
    db_port: int = Field(5432, env='DB_PORT')
    redis_host: str = Field('redis_auth', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    auth_port: int = Field(5000, env='AUTH_PORT')

auth_config = AuthSettings()

class Config(object):
    DEBUG = False

    CSRF_ENABLED = True

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


config = Config()