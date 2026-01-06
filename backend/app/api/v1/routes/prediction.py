from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.schemas.transaction import TransactionInput, PredictionResponse
from app.services.deteccao import detector
from app.core.database import get_session
from app.models.transaction import Transaction
from app.repositories.transactions_repository import TransactionsRepository

router = APIRouter(
    prefix="/predict",
    tags=["Predição"]
)


@router.post("", response_model=PredictionResponse)
def predict_transaction(
    request: TransactionInput,
    session: Session = Depends(get_session)
):
    if detector.model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo de fraude não carregado"
        )

    try:
        result = detector.predict_transaction(request.features)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao executar modelo: {exc}"
        )

    transaction = Transaction(
        **request.features,
        prediction=-1 if result["is_fraud"] else 1,
        risk_score=result["probability"],
        risk_level=result["risk_level"]
    )

    repo = TransactionsRepository(session)
    repo.create(transaction)

    return result