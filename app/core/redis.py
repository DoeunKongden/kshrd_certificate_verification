from typing import Optional
from redis.asyncio import Redis, from_url
from app.core.config import settings
from app.services.user_service import UserService

# Global Redis client instance
redis_client: Optional[Redis] = None


def get_user_service() -> UserService:
    """Dependency function to get UserService instance with Redis client"""
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Make sure the app has started.")
    return UserService(redis_client)


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    redis_client = await from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=False,  # We're storing JSON strings
    )
    print("✓ Redis connected")


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        print("✓ Redis disconnected")