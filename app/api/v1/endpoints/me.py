from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.api.deps import get_keycloak_service
from app.db.database import get_db
from app.services.keycloak_service import KeycloakService
from app.services.certificate_service import CertificateService
from app.schemas.user import UserProfile
from app.schemas.certificate import CertificateListItem
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def get_certificate_service(
    db: AsyncSession = Depends(get_db),
    keycloak: KeycloakService = Depends(get_keycloak_service),
) -> CertificateService:
    return CertificateService(db=db, keycloak=keycloak)


@router.get("/", response_model=UserProfile, summary="Get current user profile")
async def get_me(
    current_user: dict = Depends(get_current_user),
    keycloak: KeycloakService = Depends(get_keycloak_service),
):
    """Returns the full user profile from Keycloak for the authenticated user."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    profile = await keycloak.get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


@router.get(
    "/certificates",
    response_model=list[CertificateListItem],
    summary="Get current user's certificates",
)
async def get_my_certificates(
    current_user: dict = Depends(get_current_user),
    service: CertificateService = Depends(get_certificate_service),
):
    """Returns all certificates issued to the authenticated user."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    certs = await service.get_by_user_id(user_id)
    return [CertificateListItem(**c) for c in certs]
