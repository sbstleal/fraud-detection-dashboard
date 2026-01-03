from fastapi import APIRouter
from datetime import datetime

from app.core.config import settings
from app.services.deteccao import detector

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    model_ok = detector.model is not None
    data_ok = detector.df is not None

    return {
        "status": "ok" if (model_ok and data_ok) else "unavailable",
        "service": settings.APP_NAME,
        "model_loaded": model_ok,
        "data_loaded": data_ok,
        "total_records": len(detector.df) if data_ok else 0,
        "timestamp": datetime.utcnow()
    }