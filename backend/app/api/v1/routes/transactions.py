from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.transactions_repository import TransactionsRepository
from app.schemas.transaction import (
    TransactionFilter,
    PaginatedTransactionsResponse
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transações"]
)


@router.get("", response_model=PaginatedTransactionsResponse)
def list_transactions(
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    filters: TransactionFilter = Depends(),
    session: Session = Depends(get_session)
):
    repo = TransactionsRepository(session)

    total, items = repo.list_with_filters(
        limit=limit,
        offset=offset,
        is_fraud=filters.is_fraud,
        risk_level=filters.risk_level,
        min_risk_score=filters.min_risk_score,
        max_risk_score=filters.max_risk_score,
        min_amount=filters.min_amount,
        max_amount=filters.max_amount,
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }
