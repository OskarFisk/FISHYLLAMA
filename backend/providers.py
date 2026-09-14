import httpx
from backend.config import settings

class ProviderError(Exception): pass
class BaseProvider:
    name = "base"
    async def chat(self, messages, model): raise NotImplementedError

class OpenAICompatibleProvider(BaseProvider):
    def __init__(self, name, base_url, api_key): self.name,self.base_url,self.api_key=name,base_url.rstrip('/'),api_key
    async def chat(self, messages, model):
        if not self.api_key: raise ProviderError(f"{self.name} API key is not configured")
        async with httpx.AsyncClient(timeout=120) as client:
            r=await client.post(f"{self.base_url}/chat/completions",headers={"Authorization":f"Bearer {self.api_key}"},json={"model":model,"messages":messages})
            r.raise_for_status(); return r.json()["choices"][0]["message"]["content"]

class OllamaProvider(BaseProvider):
    name="ollama"
    async def chat(self,messages,model):
        async with httpx.AsyncClient(timeout=180) as client:
            r=await client.post(f"{settings.ollama_url.rstrip('/')}/api/chat",json={"model":model,"messages":messages,"stream":False})
            r.raise_for_status(); return r.json()["message"]["content"]

PROVIDERS={
 "openai":OpenAICompatibleProvider("openai","https://api.openai.com/v1",settings.openai_api_key),
 "deepseek":OpenAICompatibleProvider("deepseek","https://api.deepseek.com/v1",settings.deepseek_api_key),
 "xai":OpenAICompatibleProvider("xai","https://api.x.ai/v1",settings.xai_api_key),
 "groq":OpenAICompatibleProvider("groq","https://api.groq.com/openai/v1",settings.groq_api_key),
 "mistral":OpenAICompatibleProvider("mistral","https://api.mistral.ai/v1",settings.mistral_api_key),
 "ollama":OllamaProvider(),
}
