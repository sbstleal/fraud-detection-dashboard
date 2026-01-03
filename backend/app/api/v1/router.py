from fastapi import APIRouter

from app.api.v1.routes import prediction, anomalies, kpis

api_router = APIRouter()

api_router.include_router(prediction.router)
api_router.include_router(anomalies.router)
api_router.include_router(kpis.router)
