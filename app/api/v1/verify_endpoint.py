from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.user_service import UserService
from app.services.certificate_service import CertificateService
from ..deps.deps import get_cert_service, get_user_service



router = APIRouter(prefix="/verify", tags=["Verification"])


@router.get("/{verify_code}")
async def verify_certificate(
    verify_code: str,
    cert_service: CertificateService = Depends(get_cert_service),
    user_service: UserService = Depends(get_user_service),
):
    # 1. Ask the CertificateService to find the record in Postgres
    cert = await cert_service.get_by_code(verify_code)

    if not cert:
        # If the service returned None (due to error or missing record)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found. Please check the verification code."
        )


    # 2. Use the user_id from the cert to get the student profile
    student_profile = await user_service.get_user_profile(cert.user_id)

    if not student_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated student profile could not be retrieved."
        )


    # 3. Return a clean, unified response
    return {
        "verified": True,
        "certificate_details": {
            "code": cert.verify_code,
            "type": cert.type_id,
            "issued_at": cert.created_at
        },
        "student_profile": student_profile.model_dump_json()
    }