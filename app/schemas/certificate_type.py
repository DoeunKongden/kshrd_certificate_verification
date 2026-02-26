from pydantic import BaseModel, ConfigDict, UUID4, Field, field_validator
from typing import Optional, List, Any
from app.schemas.certificate_template import TemplateElement


class CertificateTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    target_role: str = Field(default="STUDENT", pattern="^(STUDENT|STAFF)$")
    template_id: Optional[UUID4] = None


class CertificateTypeCreate(CertificateTypeBase):
    pass


class CertificateTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = None
    target_role: Optional[str] = Field(None, pattern="^(STUDENT|STAFF)$")
    template_id: Optional[UUID4] = None


class TemplateInfo(BaseModel):
    id: UUID4
    name: str
    layout_config: List[TemplateElement] = []

    model_config = ConfigDict(from_attributes=True)

    @field_validator('layout_config', mode='before')
    @classmethod
    def convert_layout_config(cls, v):
        if v is None:
            return []
        if isinstance(v, dict):
            return []
        return v


class CertificateTypeRead(CertificateTypeBase):
    id: int
    template: Optional[TemplateInfo] = None

    model_config = ConfigDict(from_attributes=True)
