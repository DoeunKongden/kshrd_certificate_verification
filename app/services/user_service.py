from typing import Optional
from redis.asyncio import Redis
from app.services.redis_service import RedisService
from app.services.keycloak_service import KeycloakService
from app.schemas.user import UserProfile


class UserService:
    """
    Service that combine the keycloak and redis service.
    Check cache in redis first, then Keycloak if not found cache in redis
    """

    def __init__(self, redis_client: Redis):
        self.redis_service = RedisService(redis_client)
        self.keycloak_service = KeycloakService()

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile with caching:
        1. Try Redis cache first
        2. If not found, fetch from Keycloak
        3. Cache the result in Redis
        4. Return the profile
        """

        cached_profile = await self.redis_service.get_user(user_id)

        if cached_profile:
            print(f"✓ Cache HIT for user {user_id}")
            return cached_profile

        print(f"✗ Cache MISS for user {user_id}")
        profile = await self.keycloak_service.get_user_profile(user_id)

        if profile:
            await self.redis_service.set_user(user_id,profile=profile)
            print(f"✓ Cached user {user_id} in Redis")

        return profile
