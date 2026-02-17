from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional, Dict, Any


class TemplateRead(BaseModel):
    """
    Schemas for responding and reading the tempate layout configuration
    """
    id: UUID4
    name: str
    description: Optional[str] = None

    # Layout configuration
    layout_config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)