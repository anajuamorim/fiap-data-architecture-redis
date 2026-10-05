import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    username: str | None = os.getenv("REDIS_USERNAME") or None
    password: str | None = os.getenv("REDIS_PASSWORD") or None
    db: int = int(os.getenv("REDIS_DB", "0"))


config = RedisConfig()
