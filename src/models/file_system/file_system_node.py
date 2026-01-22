import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from src.db.base import PG_Base

class FileSystemNode(PG_Base):
    # class-level config attr used by sqlalchemy
    __tablename__ = "file_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # file / folder
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("file_nodes.id", ondelete="CASCADE"),
        nullable=True
    ) # point to parent node

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    children = relationship(
        "FileSystemNode",
        cascade="all, delete-orphan", # to handle automatically the children deletion
        passive_deletes=True,
        backref=backref("parent", remote_side=[id])
    )
    document = relationship(
        "Document",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="file_node"
    )

