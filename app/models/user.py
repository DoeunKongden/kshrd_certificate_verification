from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    # Primary Key: Must match the 'sub' field from Keycloak
    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, unique=True, nullable=False)
    
    # Logic fields
    role = Column(String, server_default="GRADUATE") # e.g., ADMIN, STAFF, GRADUATE
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, server_default=text("now()"), onupdate=datetime.utcnow)

    # Relationships: One user can have many certificates
    certificates = relationship("Certificate", back_populates="owner", cascade="all, delete-orphan")