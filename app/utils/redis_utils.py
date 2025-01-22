import redis
import json
from app.config import config


redis_client = redis.Redis(
    host=config.REDIS_HOST, 
    port=config.REDIS_PORT, 
    db=0, 
)

def get_cache(key: str):
    """
    Retrieve cached data by key.
    Returns None if not found.
    """
    return redis_client.get(key)

def set_cache(key: str, value, expire: int = 300):
    """
    Set a cache value with an optional expiration time (in seconds).
    """
    redis_client.setex(key, expire, value)

def delete_cache(key: str):
    """
    Delete a cached key if needed.
    """
    redis_client.delete(key)
