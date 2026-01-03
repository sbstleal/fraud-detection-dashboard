from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.transactions_repository import TransactionsRepository

router = APIRouter(
    prefix="/transactions",
    tags=["Transações"]
)

@router.get("/")
def list_transactions(
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    data = TransactionsRepository.list(session, limit, offset)
    total = TransactionsRepository.count(session)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": data
    }
