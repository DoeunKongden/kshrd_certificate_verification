from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date
from app.schemas.template import TemplateRead
from app.schemas.curriculum import SubjectDetail
from typing import Optional

class CertificateVerifyResponse(BaseModel):
    """The 'Contract' for the public verification page"""
    certificate_number: str
    issued_date: date
    verify_code: str

    # Identify between staff and student
    target_role: str 

    # UI Layout Config
    template: Optional[TemplateRead] = None

    # Detail of academic data
    subject_detail: Optional[SubjectDetail] = None

    # Holder of the information
    student_name: str
    student_photo: Optional[str] = None
    generation_name: str



    model_config = ConfigDict(from_attributes=True)