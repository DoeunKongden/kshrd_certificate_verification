from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID
from app.schemas.curriculum import SubjectDetail
from typing import Optional, List, Dict, Any


class CertificateListItem(BaseModel):
    """Summary of a certificate for list views (e.g. student's certificates)"""
    id: UUID
    certificate_number: str
    issued_date: date
    verify_code: str
    type_name: str
    target_role: str

    model_config = ConfigDict(from_attributes=True)


class CertificateData(BaseModel):
    """Certificate data portion containing student info, issue date, and verification code"""
    certificate_number: str
    issued_date: date
    verify_code: str
    target_role: str
    subject_detail: Optional[SubjectDetail] = None
    student_name: str
    student_photo: Optional[str] = None
    generation_name: str


class CertificateVerifyResponse(BaseModel):
    """The 'Contract' for the public verification page"""
    certificate_data: CertificateData
    layout_config: List[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)