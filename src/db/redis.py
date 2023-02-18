import redis

# TODO перенести в конфиги
REFRESH_TOKEN_EXPIRATION_TIME = 15 * 60


class RedisConnector:
    def __init__(self, redis_host, redis_port):
        self.db = redis.Redis(host=redis_host, port=redis_port)

    def set_user_refresh_token(self, user_id: str, refresh_token: str):
        key = self.generate_user_refresh_token_key(user_id)
        self.db.set(key, refresh_token, ex=REFRESH_TOKEN_EXPIRATION_TIME)

    def delete_user_refresh_token(self, user_id):
        key = self.generate_user_refresh_token_key(user_id)
        self.db.delete(key)

    @staticmethod
    def generate_user_refresh_token_key(user_id: str):
        return f"{user_id}_refresh_token"


redis_client = RedisConnector('127.0.0.1', '6379')  # TODO заменить на конфиги