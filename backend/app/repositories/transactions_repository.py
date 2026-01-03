from typing import List
from sqlmodel import Session, select, func

from app.models.transaction import Transaction


class TransactionsRepository:
    """
    Repository responsável por todas as operações
    de acesso a dados da entidade Transaction.
    """

    def __init__(self, session: Session):
        self.session = session

    # =========================
    # ESCRITA
    # =========================

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def bulk_create(self, transactions: List[Transaction]) -> None:
        self.session.add_all(transactions)
        self.session.commit()

    # =========================
    # LEITURA
    # =========================

    def list(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Transaction]:
        statement = (
            select(Transaction)
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def list_anomalies(
        self,
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
        return self.session.exec(statement).all()

    # =========================
    # MÉTRICAS BÁSICAS
    # =========================

    def count(self) -> int:
        statement = select(func.count(Transaction.id))
        return self.session.exec(statement).one()

    def count_anomalies(self) -> int:
        statement = (
            select(func.count(Transaction.id))
            .where(Transaction.prediction == -1)
        )
        return self.session.exec(statement).one()
