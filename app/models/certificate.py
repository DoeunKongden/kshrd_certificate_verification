import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    certificate_number = Column(String(100), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="RESTRICT"))
    type_id = Column(Integer, ForeignKey("certificate_types.id", ondelete="RESTRICT"))
    
    issued_date = Column(Date, nullable=False)
    verify_code = Column(String(100), unique=True, index=True, nullable=False)
    digital_url = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="certificates")
    subject = relationship("Subject", back_populates="certificates")

    # CRITICAL : this allow cert.type.target_role and cert.type.template.name
    type = relationship("CertificateType", back_populates="certificates")

    def __repr__(self):
        return f"<Certificate {self.certificate_number} - {self.verify_code}>"