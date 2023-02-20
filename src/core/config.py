import datetime

from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    db_name: str = os.getenv('DB_NAME', 'database_auth')
    pg_user: str = os.getenv('POSTGRES_USER', 'app')
    pg_password: str = os.getenv('POSTGRES_PASSWORD', 'qwerty123') 
    db_host: str = os.getenv( 'POSTGRES_HOST', 'postgres')
    db_port: int = os.getenv('DB_PORT', 5432)
    redis_host: str = os.getenv('REDIS_HOST', 'redis_auth')
    redis_port: int = os.getenv('REDIS_PORT', 6379)
    auth_port: int = os.getenv('AUTH_PORT', 5555)


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
