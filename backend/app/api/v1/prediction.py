from fastapi import APIRouter, HTTPException
from app.schemas.transaction import TransactionInput, PredictionResponse
from app.services.deteccao import detector

router = APIRouter(
    prefix="/api/v1",
    tags=["Predição"]
)

@router.post("/predict", response_model=PredictionResponse)
def predict_transaction(request: TransactionInput):
    """
    Analisa uma transação financeira e retorna o risco de fraude.
    """
    result = detector.predict_transaction(request.features)

    if result.get("error"):
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a transação"
        )

    return result
