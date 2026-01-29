from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.services.chat.llm_service import LLMService

_llama = ChatOllama(
    model="llama3",
    base_url="http://localhost:11434"
)
_embedding_model_instance = None

_llm_service = LLMService(_llama)

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