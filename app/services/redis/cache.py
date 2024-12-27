import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def set_cache(key: str, value: str, expire: int = 3600):
    return redis_client.setex(key, expire, value)

def get_cache(key: str):
    return redis_client.get(key)

def delete_cache(key: str):
    return redis_client.delete(key) 