from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    GROQ_API_KEY:str
    DATABASE_URL_SYNC:str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()