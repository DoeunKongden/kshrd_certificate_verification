from pydantic import BaseModel, ConfigDict
from typing import List 

class TopicBase(BaseModel):
    name: str
    sort_order: int

    model_config = ConfigDict(from_attributes=True)


class SubjectDetail(BaseModel):
    id: int
    name: str
    level: str 
    topics: List[TopicBase]

    model_config = ConfigDict(from_attributes=True)