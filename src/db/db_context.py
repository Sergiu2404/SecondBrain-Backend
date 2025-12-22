from sqlalchemy import create_engine, text

from src.config.config import PG_CONNECTION_STRING


engine = create_engine(PG_CONNECTION_STRING)

def test_connection():
    with engine.connect() as pg_connection:
        result = pg_connection.execute(text("select version();"))
        print(result.fetchone())