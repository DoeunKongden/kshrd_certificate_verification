from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    level = Column(String(20)) # e.g., 'BASIC' or 'ADVANCED'

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="subject")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    sort_order = Column(Integer, default=0)

    subject = relationship("Subject", back_populates="topics")