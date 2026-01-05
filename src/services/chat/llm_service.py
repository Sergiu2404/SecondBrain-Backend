class LLMService:
    async def get_response(self, prompt: str):
        return f"llama responds to {prompt}"