from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import CertificateNotFoundError
from app.models.certificate import Certificate
from app.models.certificate_type import CertificateType
from app.models.curriculum import Subject
import logging


logger = logging.getLogger(__name__)



class CertificateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_code(self, code: str):
        """Find a certificate in postgresql by it code"""

        if not code:
            raise ValueError("Verification code cannot be empty.")

        try:
            query = (
                select(Certificate)
                .where(Certificate.verify_code == code)
                .options(
                    selectinload(Certificate.type).selectinload(CertificateType.template),
                    selectinload(Certificate.subject).selectinload(Subject.topics)
                )
            )

            result = await self.db.execute(query)
            cert = result.scalar_one_or_none()

            if cert is None:
                raise CertificateNotFoundError(code)

            return cert

        except (CertificateNotFoundError, ValueError):
            raise


        except SQLAlchemyError as e:
            logger.error(f"Database error during certificate lookup: {e}")
            raise ConnectionError("Database service is currently unavailable or down.")
        
        except Exception as e:
            logger.critical(f"Unexpected error in Certificate Service: {e}")
            raise
