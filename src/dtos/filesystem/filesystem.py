from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class FIleSystemNodeResponseDTO(BaseModel):
    id: UUID
    name: str
    type: str
    parent_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)