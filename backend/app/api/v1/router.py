from fastapi import APIRouter

from app.api.v1.routes import prediction, kpis, anomalies

api_router = APIRouter()

# Rotas de Predição (ML)
api_router.include_router(prediction.router)

# Rotas de KPIs / Dashboard
api_router.include_router(kpis.router)

# Rotas de Anomalies
api_router.include_router(anomalies.router)