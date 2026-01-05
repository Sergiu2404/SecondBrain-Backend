import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql.base import UUID

from src.db.base import PG_Base

class Document(PG_Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_node_id = Column(UUID(as_uuid=True), ForeignKey("file_nodes.id"))
    document_type = Column(String)
    storage_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)