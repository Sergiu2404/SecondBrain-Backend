from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.db.base import PG_Base
from src.models.documents import document
from src.models.documents import document_chunk
from src.models.file_system import file_system_node
from src.models.chat import chat, message

from src.models.documents.document import Document
from src.models.documents.document_chunk import DocumentChunk
from src.models.file_system.file_system_node import FileSystemNode
from src.models.chat.chat import Chat
from src.models.chat.message import Message
from src.config import config

postgres_engine = create_engine(config.PG_CONNECTION_STRING) # connectivity to postgres
print(config.PG_CONNECTION_STRING)
SessionLocal = sessionmaker(bind=postgres_engine, autocommit=False, autoflush=False) # sessions creation factory

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostgresDatabaseContext:
    def __init__(self, engine):
        self.__engine = engine

    def test_connection(self):
        with self.__engine.connect() as pg_connection:
            result = pg_connection.execute(text("select version();"))
            print(result.fetchall())

    def init_tables(self):
        '''
        Create tables if they don't alreayd exist
        '''
        with self.__engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()
        print(f"Tables found in metadata: {PG_Base.metadata.tables.keys()}")
        PG_Base.metadata.create_all(self.__engine)