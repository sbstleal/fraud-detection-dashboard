from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()