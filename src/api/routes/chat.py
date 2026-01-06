from datetime import datetime
from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.orm import Session

from src.db.db_context import get_db
from src.repositories.chat.chat_repository import ChatRepository
from src.services.chat.chat_service import ChatService
from src.services.chat.llm_service import LLMService

router = APIRouter()
chat_repo = ChatRepository()
chat_service = ChatService(chat_repo)
llm_service = LLMService()

class ChatMessageDTO(BaseModel):
    content: str
    chat_id: UUID

class ChatDTO(BaseModel):
    title: str

class ChatResponseDTO(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class ChatMessageResponseDTO(BaseModel):
    id: UUID
    role: str
    content: str
    sequence: int
    created_at: datetime
    chat_id: UUID

    model_config = {"from_attributes": True}




@router.post("/send-message")
async def send_message(message: ChatMessageDTO, session: Session = Depends(get_db)): #
    # breakpoint()
    new_message = chat_service.create_message(session, chat_id=message.chat_id, role="user", content=message.content)
    llm_response = await llm_service.get_response(new_message.content)
    llm_message = chat_service.create_message(session, chat_id=message.chat_id, role="assistant", content=llm_response)

    return {"response": f"sent {new_message.content}, LLM answered with: {llm_message.content}"}

@router.post("/create-chat", response_model=ChatResponseDTO, status_code=status.HTTP_201_CREATED)
def create_chat(session: Session = Depends(get_db)):
    new_chat = chat_service.create_chat(session)
    return new_chat

@router.get("/latest-chat", response_model=ChatResponseDTO, status_code=status.HTTP_200_OK)
def get_latest_chat(session: Session = Depends(get_db)):
    new_chat = chat_service.get_latest_chat(session)
    return new_chat

@router.get("/chat-messages/{chat_id}", response_model=List[ChatMessageResponseDTO], status_code=status.HTTP_200_OK)
def get_chat_messages(chat_id: UUID, session: Session = Depends(get_db)):
    messages = chat_service.get_messages_by_chat(session, chat_id=chat_id)
    return messages