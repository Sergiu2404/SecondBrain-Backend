from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.db.db_context import PostgresDatabaseContext, postgres_engine
from src.api.routes import chat

origins = [
    "http://localhost:5173",
    "http://localhost:5174"
]

@asynccontextmanager
async def lifespan():
    pg_db_context = PostgresDatabaseContext(postgres_engine)
    pg_db_context.test_connection()
    pg_db_context.init_tables()

    yield # app runs here

    # closing db connections here

app = FastAPI(title="Second-Brain API")

@app.get("/ping")
def ping():
    return {"status": "response"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chats")
