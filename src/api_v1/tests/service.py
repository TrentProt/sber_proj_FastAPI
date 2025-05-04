from src.core.redis import redis_client


def redis_helper(redis_key: str, time_expire: int, arg: list):
    redis_client.delete(redis_key)
    redis_client.rpush(redis_key, *arg)
    redis_client.expire(redis_key, time_expire)
