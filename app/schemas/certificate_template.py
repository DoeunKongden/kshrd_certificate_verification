from pydantic import BaseModel, ConfigDict, UUID4, Field, field_validator
from typing import Optional, List, Dict, Any

# 1. The structural "rules" for a single UI element (text, image, signature)
class TemplateElement(BaseModel):
    type: str = Field(..., description="e.g., 'text', 'image', 'qr_code'")
    label: str = Field(..., description="The internal name like 'student_name'")
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    width: Optional[int] = None
    height: Optional[int] = None
    style: Optional[Dict[str, Any]] = None # For custom CSS or font properties

# 2. Base Schema (Shared fields)
class TemplateBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    # Best Practice: Define layout_config as a List of elements rather than a generic Dict
    layout_config: List[TemplateElement]

# 3. Create Schema (What the Admin sends to POST /templates)
class TemplateCreate(TemplateBase):
    pass

# 4. Read Schema (What the API returns)
class TemplateRead(TemplateBase):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)

    @field_validator('layout_config', mode='before')
    @classmethod
    def convert_layout_config(cls, v):
        if v is None:
            return []
        if isinstance(v, dict):
            return []
        return v

# 5. Update Schema
class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    layout_config: Optional[List[TemplateElement]] = None