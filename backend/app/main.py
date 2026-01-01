from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.services.deteccao import detector
from app.schemas.transaction import TransactionInput, PredictionResponse

app = FastAPI(
    title="Fraud Detection API",
    description="API para detecção de transações financeiras suspeitas usando Machine Learning.",
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de saúde da aplicação."""
    return {
        "status": "ok",
        "service": "fraud-detection-api",
        "model_loaded": detector.model is not None,
        "timestamp": datetime.utcnow()
    }

@app.post(
    "/api/v1/predict",
    response_model=PredictionResponse,
    tags=["Prediction"]
)
def predict(request: TransactionInput):
    """
    Analisa uma transação financeira e retorna o risco de fraude.

    - Recebe features normalizadas da transação
    - Retorna score de risco e classificação
    """

    result = detector.predict_transaction(request.features)

    if result.get("error"):
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a transação"
        )

    return result