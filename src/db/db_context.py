from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.db.base import PG_Base
from src.models.documents import document
from src.models.documents import document_chunk
from src.models.file_system import file_system_node
from src.models.chat import chat, message
from src.config import config

postgres_engine = create_engine(config.PG_CONNECTION_STRING)
SessionLocal = sessionmaker(bind=postgres_engine, autocommit=False, autoflush=False)

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
        PG_Base.metadata.create_all(self.__engine)