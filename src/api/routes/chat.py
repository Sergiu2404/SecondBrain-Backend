from typing import List, Optional
from fastapi import APIRouter, status
from fastapi.params import Depends
from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from sqlalchemy.orm import Session

from src.db.db_context import get_db
from src.dtos.chat.chat import ChatResponseDTO
from src.dtos.chat.message import ChatMessageDTO, ChatMessageResponseDTO
from src.models.chat.chat import Chat
from src.services.chat.llm_service import LLMService
from src.api.dependencies import get_llm_service, get_embedding_model, get_chat_service, get_filesystem_service

router = APIRouter()
chat_service = get_chat_service()
filesystem_service = get_filesystem_service()

@router.get("/debug/chats")
def debug_chats(db: Session = Depends(get_db)):
    return db.query(Chat).all()


@router.get("", response_model=List[ChatResponseDTO], status_code=status.HTTP_200_OK)
def get_chats(session: Session = Depends(get_db)):
    chats = chat_service.get_chats(session)
    return chats

@router.post("/send-message")
async def send_message(
        message: ChatMessageDTO,
        session: Session = Depends(get_db),
        llm_service: LLMService = Depends(get_llm_service),
        embedding_model: OllamaEmbeddings = Depends(get_embedding_model)
): #
    new_message = chat_service.create_message(session, chat_id=message.chat_id, role="user", content=message.content)
    query_vector = await embedding_model.aembed_query(message.content)

    similar_chunks = filesystem_service.get_similar_chunks(session, query_vector, limit=4)
    context_text = "\n\n".join([chunk.text for chunk in similar_chunks])

    if chat_service.is_first_user_message_in_chat(session, message.chat_id):
        title = await llm_service.generate_chat_title(message.content)
        chat_service.update_chat_title(session, message.chat_id, title)

    limited_chat_messages = chat_service.get_messages_by_chat(session, chat_id=message.chat_id, limit=5)

    # llm_response = await llm_service.get_response(limited_chat_messages)
    llm_response = await llm_service.get_response_with_context(
        question=message.content,
        context=context_text,
        limited_chat_history=limited_chat_messages
    )
    llm_message = chat_service.create_message(session, chat_id=message.chat_id, role="assistant", content=llm_response)

    return {"response": llm_message.content}

@router.post("/create-chat", response_model=ChatResponseDTO, status_code=status.HTTP_201_CREATED)
def create_chat(session: Session = Depends(get_db)):
    new_chat = chat_service.create_chat(session)
    return new_chat

@router.get("/latest-chat", response_model=Optional[ChatResponseDTO], status_code=status.HTTP_200_OK)
def get_latest_chat(session: Session = Depends(get_db)):
    new_chat = chat_service.get_latest_chat(session)
    return new_chat

@router.get("/chat-messages/{chat_id}", response_model=List[ChatMessageResponseDTO], status_code=status.HTTP_200_OK)
def get_chat_messages(chat_id: UUID, session: Session = Depends(get_db)):
    messages = chat_service.get_messages_by_chat(session, chat_id=chat_id, limit=None)
    return messages