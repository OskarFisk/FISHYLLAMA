from backend.providers import PROVIDERS, ProviderError
DEFAULT_MODELS={"openai":"gpt-5","deepseek":"deepseek-chat","xai":"grok-4","groq":"llama-4-scout-17b-16e-instruct","mistral":"mistral-large-latest","ollama":"llama3.2"}
class ModelRouter:
    def available(self): return list(PROVIDERS)
    def choose(self,requested):
        if requested in PROVIDERS:return requested
        for name,p in PROVIDERS.items():
            if name!="ollama" and getattr(p,"api_key",None):return name
        return "ollama"
    async def chat(self,messages,requested="auto",model=None):
        name=self.choose(requested); selected=model or DEFAULT_MODELS[name]
        try:return await PROVIDERS[name].chat(messages,selected),name,selected
        except Exception as exc:
            if requested=="auto" and name!="ollama":return await PROVIDERS["ollama"].chat(messages,DEFAULT_MODELS["ollama"]),"ollama",DEFAULT_MODELS["ollama"]
            raise ProviderError(str(exc)) from exc
