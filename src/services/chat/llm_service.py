from typing import List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_ollama import ChatOllama

from src.api.routes.chat import ChatMessageDTO


class LLMService:
    SYSTEM_PROMPT = "You are a helpful assistant, reply briefly and clearly. Answer in the same language as the user."

    def __init__(self, llama: ChatOllama):
        self.__llama = llama

    async def get_response(self, limited_chat_history: List[ChatMessageDTO]):
        messages: List[BaseMessage] = [
            SystemMessage(
                content=self.SYSTEM_PROMPT
            )
        ]

        for message in limited_chat_history:
            if message.role == "user":
                messages.append(
                    HumanMessage(content=message.content)
                )
            elif message.role == "assistant":
                messages.append(
                    AIMessage(content=message.content)
                )

        llm_response = await self.__llama.ainvoke(messages)
        return llm_response.content.strip()

    async def generate_chat_title(self, first_message: str) -> str:
        messages = [
            SystemMessage(
                content=(
                    "Generate a short, clear chat title (max 6 words) for our current discussion. "
                    "No quotes. No punctuation at the end."
                )
            ),
            HumanMessage(content=first_message),
        ]

        response = await self.__llama.ainvoke(messages)
        return response.content.strip()

