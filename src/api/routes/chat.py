from typing import List
from fastapi import APIRouter, status
from fastapi.params import Depends
from langchain_ollama import ChatOllama
from uuid import UUID
from sqlalchemy.orm import Session

from src.db.db_context import get_db
from src.dtos.chat.chat import ChatResponseDTO
from src.dtos.chat.message import ChatMessageDTO, ChatMessageResponseDTO
from src.repositories.chat.chat_repository import ChatRepository
from src.services.chat.chat_service import ChatService
from src.services.chat.llm_service import LLMService

router = APIRouter()
chat_repo = ChatRepository()
chat_service = ChatService(chat_repo)

# llama = Ollama(model="llama3", base_url="http://localhost:11434")
llama = ChatOllama(
    model="llama3",
    base_url="http://localhost:11434"
)
llm_service = LLMService(llama)



@router.get("", response_model=List[ChatResponseDTO], status_code=status.HTTP_200_OK)
def get_chats(session: Session = Depends(get_db)):
    chats = chat_service.get_chats(session)
    return chats

@router.post("/send-message")
async def send_message(message: ChatMessageDTO, session: Session = Depends(get_db)): #
    new_message = chat_service.create_message(session, chat_id=message.chat_id, role="user", content=message.content)

    if chat_service.is_first_user_message_in_chat(session, message.chat_id):
        title = await llm_service.generate_chat_title(message.content)
        chat_service.update_chat_title(session, message.chat_id, title)

    limited_chat_messages = chat_service.get_messages_by_chat(session, chat_id=message.chat_id, limit=5)

    llm_response = await llm_service.get_response(limited_chat_messages)
    llm_message = chat_service.create_message(session, chat_id=message.chat_id, role="assistant", content=llm_response)

    return {"response": llm_message.content}

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
    messages = chat_service.get_messages_by_chat(session, chat_id=chat_id, limit=None)
    return messages