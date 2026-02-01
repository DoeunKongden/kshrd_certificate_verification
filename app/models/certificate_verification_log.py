from sqlalchemy import Column, String, DateTime, ForeignKey, Text,text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import foreign, relationship
from app.db.database import Base
import uuid

class VerificationLog(Base):
    __tablename__ = "certificate_verification_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_id = Column(UUID(as_uuid=True), ForeignKey("certificates.id", ondelete="CASCADE"))

    ip_address = Column(String(45))
    user_aget = Column(Text)
    status = Column(String(20),default="SUCCESS")
    verified_at = Column(DateTime, server_default=text("now()"))

    metadata = Column(JSONB, nullable=True)

    certificate = relationship("Certificate", back_populates="logs")