from src.models.chat.chat import Chat
from src.models.chat.message import Message
from src.repositories.chat.chat_repository import ChatRepository
from sqlalchemy.dialects.postgresql import UUID

class ChatService:
    def __init__(self, repo: ChatRepository = None):
        self.__repo = repo or ChatRepository()

    def create_message(self, session, chat_id: UUID, role: str, content: str):
        last_message = self.__repo.get_last_message_in_chat(session, chat_id)
        sequence = last_message.sequence + 1 if last_message else 1

        message = Message(role=role, content=content, sequence=sequence, chat_id=chat_id)
        return self.__repo.save_message(session, message)

    def create_chat(self, session):
        chat = Chat(title="New Chat")
        return self.__repo.create_chat(session, chat)

    def get_messages_by_chat(self, session, chat_id: UUID):
        return self.__repo.get_messages_by_chat(session, chat_id)

    def get_latest_chat(self, session):
        return self.__repo.get_latest_chat(session)