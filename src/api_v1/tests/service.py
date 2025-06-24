from src.core.redis import redis_client


async def redis_helper(redis_key: str, time_expire: int, arg: list):
    await redis_client.delete(redis_key)
    await redis_client.rpush(redis_key, *arg)
    await redis_client.expire(redis_key, time_expire)
