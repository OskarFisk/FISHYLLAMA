from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FishyLLAMA"
    host: str = "0.0.0.0"
    port: int = 8000
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    deepseek_api_key: str | None = None
    xai_api_key: str | None = None
    mistral_api_key: str | None = None
    groq_api_key: str | None = None
    ollama_url: str = "http://localhost:11434"
    model: str = "auto"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
