import redis

from .config import config


def get_client() -> redis.Redis:
    """Create a Redis client using environment variables."""
    return redis.Redis(
        host=config.host,
        port=config.port,
        username=config.username,
        password=config.password,
        db=config.db,
        decode_responses=True,
    )
