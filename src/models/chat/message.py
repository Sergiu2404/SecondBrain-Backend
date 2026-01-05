import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.db.base import PG_Base


class Message(PG_Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    role = Column(String, nullable=False) # user / assistant / system (system at RAG)
    content = Column(Text, nullable=False)
    sequence = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
