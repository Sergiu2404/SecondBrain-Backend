from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session

from src.db.db_context import get_db
from src.dtos.filesystem.filesystem import FIleSystemNodeResponseDTO
from src.repositories.filesystem.filesystem_repository import FileSystemRepository
from src.services.filesystem.filesystem_service import FileSystemService

router = APIRouter()
filesystem_repo = FileSystemRepository()
filesystem_service = FileSystemService(filesystem_repo)

@router.get("", status_code=status.HTTP_200_OK)
def get_nodes(session: Session = Depends(get_db)):
    return filesystem_service.get_all_nodes(session)

@router.post("/folders", response_model=FIleSystemNodeResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_folder(
    node_data: dict,
    session: Session = Depends(get_db)
):
    return await filesystem_service.create_node(
        session,
        name=node_data["name"],
        type="folder",
        parent_id=node_data.get("parent_id"),
        file=None,
    )

@router.post("/files", response_model=FIleSystemNodeResponseDTO, status_code=status.HTTP_201_CREATED)
async def upload_file(
    name: str = Form(...),
    parent_id: Optional[UUID] = Form(None),
    file: UploadFile = File(...),
    session: Session = Depends(get_db)
):
    return await filesystem_service.create_node(
        session,
        name=name,
        type="file",
        parent_id=parent_id,
        file=file
    )

@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: UUID, session: Session = Depends(get_db)):
    print(node_id)
    filesystem_service.delete_node(session, node_id)
