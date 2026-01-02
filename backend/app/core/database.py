from sqlmodel import SQLModel, create_engine, Session
# Importamos o settings que acabamos de ajustar
from app.core.config import settings

# A engine usa a URL gerada dinamicamente pelo Pydantic
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

def get_session():
    """
    Dependency para injetar a sessão do banco nas rotas.
    """
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Cria as tabelas no banco se não existirem"""
    SQLModel.metadata.create_all(engine)