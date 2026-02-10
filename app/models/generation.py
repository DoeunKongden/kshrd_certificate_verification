from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.database import Base

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    hrd_gen_id = Column(Integer, unique=True)
    name = Column(String(50), nullable=False)
    
    users = relationship("User", back_populates="generation")
    