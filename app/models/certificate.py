from sqlalchemy import Column, String, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_number = Column(String, unique=True, nullable=False)
    
    # Link to the User
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    
    course_name = Column(String, nullable=False)
    issued_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    
    # The unique string for the QR code
    verify_code = Column(String, unique=True, nullable=False, index=True)
    
    created_at = Column(DateTime, server_default=text("now()"))

    # Relationships
    owner = relationship("User", back_populates="certificates")
    logs = relationship("VerificationLog", back_populates="certificate", cascade="all, delete-orphan")