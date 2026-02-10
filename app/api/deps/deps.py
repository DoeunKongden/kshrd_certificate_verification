from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.certificate_service import CertificateService
from app.services.user_service import UserService
from app.core.redis import get_user_service as get_redis_user_service


async def get_cert_service(db: AsyncSession = Depends(get_db)) -> CertificateService:
    """
    Inject the CertificateService
    FastAPI handles the DB session lifecycle via get_db
    """
    return CertificateService(db=db)


async def get_user_service(
    user_service: UserService = Depends(get_redis_user_service)
) -> UserService:
    """
    Injects a fully-featured UserService with Redis caching and Keycloak integration.
    The UserService already has KeycloakService initialized internally.
    """
    return user_service