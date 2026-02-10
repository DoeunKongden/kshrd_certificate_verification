import email
from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import List, Optional


class UserProfile(BaseModel):
    """Data structure for redis cache and keycloak sync"""

    id: UUID
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name_en: str
    photo_url: Optional[str] = None 
    roles: List[str] = []

    # Additional user authentication
    phone_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    university: Optional[str] = None
    bacll_grade: Optional[str] = None  # Note: Keycloak uses "bacll-grade"
    khmer_name: Optional[str] = None
    province: Optional[str] = None
    dob: Optional[str] = None  # Date of birth as string from Keycloak
    education_level: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """The base model of the users table just only id"""
    id: UUID
    generation_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
