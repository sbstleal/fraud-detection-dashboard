from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.transactions_repository import TransactionsRepository

router = APIRouter(
    prefix="/anomalies",
    tags=["Análises"]
)


@router.get("")
def list_anomalies(
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    repo = TransactionsRepository(session)

    anomalies = repo.list_anomalies(
        limit=limit,
        offset=offset
    )

    total = repo.count()
    total_anomalies = repo.count_anomalies()

    percentage = (
        (total_anomalies / total) * 100
        if total > 0 else 0
    )

    return {
        "total_transactions": total,
        "total_anomalies": total_anomalies,
        "percentage": f"{percentage:.2f}%",
        "data": anomalies
    }
