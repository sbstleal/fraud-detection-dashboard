from typing import List, Optional
from sqlmodel import Session, select, func

from app.models.transaction import Transaction, RiskLevel


class TransactionsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def list_with_filters(
        self,
        limit: int,
        offset: int,
        is_fraud: Optional[bool] = None,
        risk_level: Optional[RiskLevel] = None,
        min_risk_score: Optional[float] = None,
        max_risk_score: Optional[float] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
    ) -> tuple[int, List[Transaction]]:

        statement = select(Transaction)

        if is_fraud is not None:
            statement = statement.where(
                Transaction.prediction == (-1 if is_fraud else 1)
            )

        if risk_level:
            statement = statement.where(Transaction.risk_level == risk_level)

        if min_risk_score is not None:
            statement = statement.where(Transaction.risk_score >= min_risk_score)

        if max_risk_score is not None:
            statement = statement.where(Transaction.risk_score <= max_risk_score)

        if min_amount is not None:
            statement = statement.where(Transaction.amount >= min_amount)

        if max_amount is not None:
            statement = statement.where(Transaction.amount <= max_amount)

        total = self.session.exec(
            select(func.count()).select_from(statement.subquery())
        ).one()

        items = self.session.exec(
            statement
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        ).all()

        return total, items