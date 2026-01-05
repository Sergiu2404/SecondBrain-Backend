import uuid
from sqlalchemy import Column, ForeignKey, Integer, Text, String
from sqlalchemy.dialects.postgresql.base import UUID

from src.db.base import PG_Base

class DocumentChunk(PG_Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    chunk_index = Column(Integer)
    text = Column(Text)
    vector_id = Column(String)