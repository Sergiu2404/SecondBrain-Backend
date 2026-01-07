from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ChatMessageDTO(BaseModel):
    content: str
    chat_id: UUID

class ChatMessageResponseDTO(BaseModel):
    id: UUID
    role: str
    content: str
    sequence: int
    created_at: datetime
    chat_id: UUID

    model_config = {"from_attributes": True}