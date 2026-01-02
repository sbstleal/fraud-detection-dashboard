from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)


def create_db_and_tables():
    """
    Cria todas as tabelas definidas nos models.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency para FastAPI.
    """
    with Session(engine) as session:
        yield session
