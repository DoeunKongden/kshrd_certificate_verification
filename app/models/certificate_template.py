import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class CertificateTemplate(Base):
    """Model Class for the Ceritificate Template table"""
    __tablename__ = "certificate_template"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, comment="Check: Graduation, Achievement")
    description = Column(Text)
    layout_config = Column(String, nullable=True)  # JSONB; Use String if not importing JSONB type

    # Relationship 
    certificate_types = relationship("CertificateType", back_populates="template")
