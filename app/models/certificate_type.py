from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..db.database import Base

class CertificateType(Base):
    """Model Class for the Certificate Type (e.g. Basic Course, Top 1 Excellence)"""
    __tablename__ = "certificate_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    target_role = Column(String(20), nullable=False, default="STUDENT") # 'STUDENT' or 'STAFF'
    
    # The UUID link to your new Template model
    template_id = Column(UUID(as_uuid=True), ForeignKey("certificate_template.id"))
    
    # Relationships
    template = relationship("CertificateTemplate", back_populates="certificate_types")
    certificates = relationship("Certificate", back_populates="type")