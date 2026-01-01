from fastapi import FastAPI
from datetime import datetime

from app.core.config import settings
from app.api.v1.prediction import router as prediction_router
from app.services.deteccao import detector

# Inicializa FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para detecção de transações financeiras suspeitas usando Machine Learning.",
    version="1.0.0",
    debug=settings.DEBUG
)

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de saúde da aplicação.
    Retorna status, nome do serviço, modelo carregado e timestamp.
    """
    status_code = 200 if detector.model else 503
    return {
        "status": "ok" if detector.model else "unavailable",
        "service": settings.APP_NAME,
        "model_loaded": detector.model is not None,
        "timestamp": datetime.utcnow()
    }, status_code

# Inclui rotas versionadas
app.include_router(prediction_router)
