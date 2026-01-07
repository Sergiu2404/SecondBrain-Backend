from src.models.chat.chat import Chat
from src.models.chat.message import Message
from sqlalchemy.dialects.postgresql import UUID

class ChatRepository:
    def create_chat(self, session, chat: Chat):
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

    def save_message(self, session, message: Message):
        session.add(message)
        session.commit()
        session.refresh(message)

        return message

    def get_messages_by_chat(self, session, chat_id: UUID, limit: int | None):
        query = session.query(Message).filter(Message.chat_id == chat_id)

        if limit:
            messages = query.order_by(Message.created_at.desc()).limit(limit).all()
            return messages[::-1]

        return query.order_by(Message.created_at.asc()).all()

    def get_last_message_in_chat(self, session, chat_id: UUID):
        return session.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.desc()).first()

    def get_latest_chat(self, session):
        return session.query(Chat).order_by(Chat.created_at.desc()).first()

    def get_chats(self, session):
        return session.query(Chat).order_by(Chat.created_at.desc()).all()

    def update_chat_title(self, session, chat_id: UUID, title: str):
        chat = session.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            return None
        chat.title = title

        session.commit()
        session.refresh(chat)

        return chat