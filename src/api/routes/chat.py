from fastapi import APIRouter
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

@router.post("/send")
async def send_message(message: ChatMessageDTO, session: Session = Depends(get_db)): #
    # breakpoint()
    new_message = chat_service.create_user_message(session, chat_id=message.chat_id, content=message.content)
    llm_response = await llm_service.get_response(new_message.content)
    return {"response": f"sent {new_message.content}, LLM answered with: {llm_response}"}

@router.post("/create-chat")
def create_chat(chat: ChatDTO, session: Session = Depends(get_db)):
    new_chat = chat_service.create_chat(session, chat.title)
    return {"response": f"sent {chat.title}, received: {new_chat.created_at}"}