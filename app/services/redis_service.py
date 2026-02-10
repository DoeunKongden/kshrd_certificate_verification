import json
from typing import Optional
from redis.asyncio import Redis
from app.schemas.user import UserProfile


class RedisService:
    """A Redis Class for initializing connection to the redis database"""
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.prefex = 'user_cache:'
        self.ttl = 1800 # 30mn

    
    async def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Fetch cached profile and convert back to pydantic object"""
        data = await self.redis.get(f"{self.prefex}{user_id}")
        
        if not data:
            return None

        return UserProfile.model_validate_json(data)

    async def set_user(self, user_id: str, profile: UserProfile):
        """Store the validated Pydantic profile as JSON string"""
        await self.redis.setex(
            f"{self.prefex}{user_id}",
            self.ttl,
            profile.model_dump_json()
        )