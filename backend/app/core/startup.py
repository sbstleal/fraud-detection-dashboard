import logging
from sqlalchemy import text
from sqlmodel import Session

from app.services.deteccao import detector
from app.core.database import engine

logger = logging.getLogger(__name__)


def startup_event():

    logger.info("🚀 [STARTUP] Iniciando aplicação...")

    if detector.model is None or detector.scaler is None:
        logger.error("❌ Modelo ou Scaler NÃO carregados")
    else:
        logger.info("✅ Modelo e Scaler carregados")

    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        logger.info("✅ Conexão com banco de dados OK")
    except Exception as exc:
        logger.critical(f"❌ Falha ao conectar no banco: {exc}")

    logger.info("🏁 [STARTUP] Finalizado")