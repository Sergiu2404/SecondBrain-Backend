from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.repositories.chat.chat_repository import ChatRepository
from src.repositories.filesystem.filesystem_repository import FileSystemRepository
from src.services.chat.chat_service import ChatService
from src.services.chat.llm_service import LLMService
from src.services.filesystem.filesystem_service import FileSystemService

_llama = ChatOllama(
    model="llama3",
    base_url="http://localhost:11434"
)
_embedding_model_instance = None

_chat_repo = ChatRepository()
_filesystem_repo = FileSystemRepository()

_chat_service = ChatService(_chat_repo)
_filesystem_service = FileSystemService(_filesystem_repo)

_llm_service = LLMService(_llama)


def get_chat_service() -> ChatService:
    return _chat_service

def get_filesystem_service() -> FileSystemService:
    return _filesystem_service

def get_llm_service() -> LLMService:
    return _llm_service
def get_embedding_model() -> OllamaEmbeddings:
    global _embedding_model_instance
    if _embedding_model_instance is None:
        _embedding_model_instance = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        # _embedding_model_instance = HuggingFaceEmbeddings(
        #     model_name="all-MiniLM-L6-v2",
        #     model_kwargs={"device": "cuda"}
        # )
    return _embedding_model_instance