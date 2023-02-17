import redis

from core.config import CACHE_REFRESH_TOKEN_EXPIRATION_TIME


class RedisConnector:
    def __init__(self, redis_host, redis_port):
        self.db_for_refresh = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.db_for_invalid_access = redis.Redis(host=redis_host, port=redis_port, db=1)

    def set_user_refresh_token(self, user_id: str, refresh_token: str):
        self.db_for_refresh.set(user_id, refresh_token, ex=CACHE_REFRESH_TOKEN_EXPIRATION_TIME)

    def set_user_invalid_access_token(self, user_id: str, access_token: str):
        self.db_for_invalid_access.set(user_id, access_token)
