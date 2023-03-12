from __future__ import annotations

import redis
from core.config import auth_config, CACHE_REFRESH_TOKEN_EXPIRATION_TIME


class RedisConnector:
    def __init__(self, redis_host, redis_port):
        self.db_for_refresh = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=0,
        )
        self.db_for_invalid_access = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=1,
        )

    def set_user_refresh_token(self, user_id: str, refresh_token: str):
        self.db_for_refresh.set(
            user_id,
            refresh_token,
            ex=CACHE_REFRESH_TOKEN_EXPIRATION_TIME,
        )

    def set_user_invalid_access_token(self, user_id: str, jti: str):
        self.db_for_invalid_access.set(jti, user_id)

    def check_if_access_token_is_invalid(self, jti: str) -> bool:
        return self.db_for_invalid_access.get(jti) is not None


redis_client = RedisConnector(auth_config.redis_host, auth_config.redis_port)
