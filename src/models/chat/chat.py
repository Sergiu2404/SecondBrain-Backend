import uuid
from datetime import datetime
from sqlalchemy import Column, UUID, String, DateTime

from src.db.base import PG_Base

class Chat(PG_Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String) # auto geenerated by assistant
    created_at = Column(DateTime, default=datetime.utcnow)