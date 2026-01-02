from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurações Gerais
    APP_NAME: str = "Fraud Detection API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Configurações de Banco de Dados (Lê do .env automaticamente)
    # Definimos valores padrão caso o .env não exista (exceto senha)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "" # Senha vazia por padrão se não achar no env
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "fraud_detection_db"

    # Monta a URL de conexão automaticamente
    @property
    def DATABASE_URL(self) -> str:
        # Se a senha tiver caracteres especiais, seria bom usar urllib.parse.quote_plus,
        # mas para senha simples local, isso funciona bem.
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        # Indica que deve ler o arquivo .env da raiz (ou do local onde roda o app)
        env_file = ".env"
        # Garante que lê as variáveis mesmo se o arquivo .env não existir (usa os defaults)
        env_file_encoding = 'utf-8'

settings = Settings()