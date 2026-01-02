from typing import List
from sqlmodel import Session, select

from app.models.transaction import Transaction


def create_transaction(
    session: Session,
    transaction: Transaction
) -> Transaction:
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def bulk_create_transactions(
    session: Session,
    transactions: List[Transaction]
):
    session.add_all(transactions)
    session.commit()


def list_transactions(
    session: Session,
    limit: int = 100,
    offset: int = 0
) -> List[Transaction]:
    statement = (
        select(Transaction)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


def list_anomalies(
    session: Session,
    limit: int = 100,
    offset: int = 0
) -> List[Transaction]:
    statement = (
        select(Transaction)
        .where(Transaction.prediction == -1)
        .order_by(Transaction.risk_score.desc())
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()