import json
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.core.exceptions import CertificateNotFoundError
from app.models.certificate import Certificate
from app.models.certificate_type import CertificateType
from app.models.curriculum import Subject
from app.models.user import User
from app.services.keycloak_service import KeycloakService
from app.schemas.curriculum import SubjectDetail
import logging
from app.core import redis


logger = logging.getLogger(__name__)


def _build_normalized_response(cert, student_name: str, student_photo: str | None, generation_name: str) -> dict:
    """Build a normalized dict ready for CertificateVerifyResponse from DB result."""
    layout_config = []
    if cert.type and cert.type.template and cert.type.template.layout_config is not None:
        layout_config = cert.type.template.layout_config if isinstance(cert.type.template.layout_config, list) else []

    subject_data = None
    if cert.subject:
        subject_data = SubjectDetail.model_validate(cert.subject).model_dump(mode="json")

    certificate_data = {
        "certificate_number": cert.certificate_number,
        "issued_date": cert.issued_date.isoformat(),
        "verify_code": cert.verify_code,
        "target_role": cert.type.target_role if cert.type else "STUDENT",
        "subject_detail": subject_data,
        "student_name": student_name,
        "student_photo": student_photo,
        "generation_name": generation_name,
    }

    return {
        "certificate_data": certificate_data,
        "layout_config": layout_config,
    }


class CertificateService:
    def __init__(self, db: AsyncSession, keycloak: KeycloakService):
        self.db = db
        self.keycloak = keycloak

    async def get_by_code(self, code: str):
        """Find a certificate in postgresql by it code"""

        if not code:
            raise ValueError("Verification code cannot be empty.")

        cache_key = f"cert_verify:{code}"

        # Cached Hit & Cached Miss Logic
        try:
            cached_data = await redis.redis_client.get(cache_key)
            if cached_data:
                parsed = json.loads(cached_data)
                # Backward compatibility: check for new structure with certificate_data
                if parsed.get("certificate_data") is not None and parsed.get("layout_config") is not None:
                    logger.info(f"Cached Hit for code : {code}")
                    return parsed
                # Old format - fall through to DB; will repopulate cache with new format
        except Exception as e:
            logger.warning(f"Redis lookup failed: {e}")

        try:
            query = (
                select(Certificate)
                .where(Certificate.verify_code == code)
                .options(
                    joinedload(Certificate.type).joinedload(
                        CertificateType.template
                    ),
                    selectinload(Certificate.subject).selectinload(Subject.topics),
                    joinedload(Certificate.user).joinedload(User.generation),
                )
            )

            result = await self.db.execute(query)
            cert = result.scalar_one_or_none()

            if cert is None:
                raise CertificateNotFoundError(code=code)

            generation_name = "N/A"
            if cert.user and cert.user.generation:
                generation_name = cert.user.generation.name

            student_name = "User not Found"
            student_photo = None

            if cert.user_id:
                user_profile = await self.keycloak.get_user_profile(str(cert.user_id))

                if user_profile:
                    student_name = user_profile.full_name_en
                    student_photo = user_profile.photo_url

                else:
                    logger.warning(
                        f"Keycloak sync issue: User {cert.user_id} not found"
                    )

            # Build normalized response (same shape for both cache and DB paths)
            normalized = _build_normalized_response(
                cert=cert,
                student_name=student_name,
                student_photo=student_photo,
                generation_name=generation_name,
            )

            # Save to redis for future cache hits
            await redis.redis_client.setex(cache_key, 3600, json.dumps(normalized))

            return normalized

        except (CertificateNotFoundError, ValueError):
            raise

        except SQLAlchemyError as e:
            logger.error(f"Database error during certificate lookup: {e}")
            raise ConnectionError(
                f"Database service is currently unavailable or down detail: {e}"
            )

        except Exception as e:
            logger.critical(f"Unexpected error in Certificate Service: {e}")
            raise

    async def get_by_user_id(self, user_id: str) -> list:
        """Get all certificates for a user (for /me/certificates endpoint)."""
        query = (
            select(Certificate)
            .where(Certificate.user_id == UUID(user_id))
            .options(joinedload(Certificate.type))
            .order_by(Certificate.issued_date.desc())
        )
        result = await self.db.execute(query)
        certs = result.scalars().unique().all()
        return [
            {
                "id": cert.id,
                "certificate_number": cert.certificate_number,
                "issued_date": cert.issued_date,
                "verify_code": cert.verify_code,
                "type_name": cert.type.name if cert.type else "Unknown",
                "target_role": cert.type.target_role if cert.type else "STUDENT",
            }
            for cert in certs
        ]
