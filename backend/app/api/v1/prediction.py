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

    - Recebe: Features normalizadas da transação
    - Retorna: Score de risco, classificação e mensagem explicativa
    """
    # Validação extra (opcional mas profissional)
    if not detector.model:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    try:
        result = detector.predict_transaction(request.features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    # Confere se o serviço retornou erro
    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])

    return result
