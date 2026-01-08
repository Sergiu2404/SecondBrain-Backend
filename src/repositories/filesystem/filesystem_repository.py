from uuid import UUID

from src.models.documents.document import Document
from src.models.file_system.file_system_node import FileSystemNode


class FileSystemRepository:
    def get_all_nodes(self, session):
        return session.query(FileSystemNode).all()

    def save_node(self, session, node: FileSystemNode):
        session.add(node)
        session.commit()
        session.refresh(node)
        return node

    def save_document(self, session, document: Document):
        session.add(document)
        session.commit()
        return document

    def get_node_and_children(self, session, node_id: UUID):
        return session.query(FileSystemNode).filter(FileSystemNode.id == node_id).all()

    def delete_node(self, session, node_id: UUID):
        node = session.query(FileSystemNode).filter(FileSystemNode.id == node_id).first()
        if node:
            session.delete(node)
            session.commit()
        return node_id