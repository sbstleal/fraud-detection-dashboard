from fastapi import FastAPI
from datetime import datetime

from app.core.config import settings
from app.core.startup import carregar_dados_csv
from app.api.v1.prediction import router as prediction_router
from app.services.deteccao import detector


app = FastAPI(
    title=settings.APP_NAME,
    description="API para detecção de transações financeiras suspeitas.",
    version="1.0.0",
    debug=settings.DEBUG
)


# --- STARTUP ---
@app.on_event("startup")
def startup_event():
    carregar_dados_csv()


# --- HEALTH ---
@app.get("/health", tags=["Health"])
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


# --- ANOMALIAS ---
@app.get("/anomalies", tags=["Análises"])
def get_anomalies():
    if detector.df is None:
        return {"message": "Dados ainda não carregados."}

    if "prediction" not in detector.df.columns:
        return {"message": "Modelo ainda não executou predições."}

    anomalies = detector.df[detector.df["prediction"] == -1]

    return {
        "total_transactions": len(detector.df),
        "total_anomalies": len(anomalies),
        "percentage": f"{(len(anomalies) / len(detector.df)) * 100:.2f}%",
        "data": anomalies.to_dict(orient="records")
    }


# --- ROTAS VERSIONADAS ---
app.include_router(prediction_router, prefix="/api/v1")
