from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ChatDTO(BaseModel):
    title: str

class ChatResponseDTO(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }