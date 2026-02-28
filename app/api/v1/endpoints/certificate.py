from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.certificate_service import CertificateService
from app.services.keycloak_service import KeycloakService
from app.schemas.certificate import CertificateVerifyResponse
from app.api.deps import get_keycloak_service




router = APIRouter()

# Dependency Injection Factory
def get_certificate_service(
    db: AsyncSession = Depends(get_db),
    keycloak: KeycloakService = Depends(get_keycloak_service)
) -> CertificateService:
    return CertificateService(db=db, keycloak=keycloak)


@router.get(
    "/{code}/verify",
    response_model=CertificateVerifyResponse,
    summary="Verify KSHRD Certificate"
)
async def verify_certificate(
    code: str = Path(
        ...,
        description="The verification code of the certificate.",
        min_length=5,
        max_length=50,
        pattern=r"^[A-Z0-9-]+$"
    ),
    service: CertificateService = Depends(get_certificate_service)
):
    """
        Endpoint to verify KSHRD certificate.
        It combines data from Postgres and Keycloak.
    """
    result = await service.get_by_code(code=code)
    return CertificateVerifyResponse(**result)