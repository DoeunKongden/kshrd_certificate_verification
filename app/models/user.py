from sqlalchemy import Column, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    # ID matches Keycloak 'sub'
    id = Column(UUID(as_uuid=True), primary_key=True) 
    generation_id = Column(Integer, ForeignKey("generations.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    generation = relationship("Generation", back_populates="users")
    certificates = relationship("Certificate", back_populates="user") 