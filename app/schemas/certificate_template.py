from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional, Dict, Any


class TemplateRead(BaseModel):
    """
    Schema response for Dynamic UI/Layout
    """

    id: UUID4
    name: str
    description: Optional[str] = None

    # This will hold our CSS/UI variables
    layout_config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)
