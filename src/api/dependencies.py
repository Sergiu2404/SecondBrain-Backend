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

_chat_repo = ChatRepository()
_filesystem_repo = FileSystemRepository()

_embedding_model_instance = None
_chat_service_instance = None
_filesystem_service_instance = None
_llm_service_instance = None

def get_chat_service() -> ChatService:
    global _chat_service_instance
    if _chat_service_instance is None:
        _chat_service_instance = ChatService(_chat_repo)
    return _chat_service_instance

def get_filesystem_service() -> FileSystemService:
    global _filesystem_service_instance
    if _filesystem_service_instance is None:
        model = get_embedding_model()
        _filesystem_service_instance = FileSystemService(_filesystem_repo, model)
    return _filesystem_service_instance

def get_llm_service() -> LLMService:
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService(_llama)
    return _llm_service_instance

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