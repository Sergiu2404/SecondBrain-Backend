import os
import shutil
from uuid import UUID, uuid4
from fastapi import UploadFile

from src.models.documents.document import Document
from src.models.file_system.file_system_node import FileSystemNode

UPLOAD_DIR = "storage/documents"

class FileSystemService:
    def __init__(self, repo):
        self.__repo = repo
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    def get_all_nodes(self, session):
        return self.__repo.get_all_nodes(session)

    async def create_node(self, session, name: str, type: str, parent_id: UUID, file: UploadFile = None):
        node = FileSystemNode(name=name, type=type, parent_id=parent_id)
        saved_node = self.__repo.save_node(session, node)

        # if type == "file" and file:
        #     file_extension = os.path.splitext(file.filename)[1]
        #     file_name = f"{uuid4()}{file_extension}"
        #     storage_path = os.path.join(UPLOAD_DIR, file_name)
        #
        #     with open(storage_path, "wb") as buffer:
        #         shutil.copyfileobj(file.file, buffer)
        #
        #     document = Document(
        #         file_node_id=saved_node.id,
        #         document_type=file.content_type,
        #         storage_path=storage_path
        #     )
        #     self.__repo.save_document(session, document)

        return saved_node

    def delete_node(self, session, node_id: UUID):
        nodes_to_check = self.__repo.get_node_and_children(session, node_id)

        for node in nodes_to_check:
            if node.type == "file" and node.document:
                if os.path.exists(node.document.storage_path):
                    os.remove(node.document.storage_path)

        self.__repo.delete_node(session, node_id)