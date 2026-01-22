import uuid
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, Text, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.db.base import PG_Base

class DocumentChunk(PG_Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )

    chunk_index = Column(Integer)
    text = Column(Text)
    vector_id = Column(String)
    embedding = Column(Vector(768))

    document = relationship("Document", back_populates="chunks")