from fastapi import APIRouter, HTTPException

from app.schemas.transaction import TransactionInput, PredictionResponse
from app.services.deteccao import detector

router = APIRouter(
    prefix="/predict",
    tags=["Predição"]
)


@router.post("", response_model=PredictionResponse)
def predict_transaction(request: TransactionInput):
    """
    Analisa uma transação financeira e retorna o risco de fraude.
    """

    if not detector.model:
        raise HTTPException(
            status_code=503,
            detail="Modelo de fraude não carregado"
        )

    try:
        result = detector.predict_transaction(request.features)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(exc)}"
        )

    if result.get("error"):
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return result