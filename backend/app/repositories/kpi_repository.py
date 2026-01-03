from typing import Dict, List
from datetime import date

from sqlmodel import Session, select, func

from app.models.transaction import Transaction


class KPIRepository:
    """
    Repository responsável por queries agregadas (KPIs)
    usadas no Dashboard e relatórios.
    """

    @staticmethod
    def total_transactions(session: Session) -> int:
        statement = select(func.count(Transaction.id))
        return session.exec(statement).one()

    @staticmethod
    def total_anomalies(session: Session) -> int:
        statement = select(func.count(Transaction.id)).where(
            Transaction.prediction == -1
        )
        return session.exec(statement).one()

    @staticmethod
    def anomaly_rate(session: Session) -> float:
        total = KPIRepository.total_transactions(session)
        if total == 0:
            return 0.0

        anomalies = KPIRepository.total_anomalies(session)
        return round((anomalies / total) * 100, 2)

    @staticmethod
    def risk_distribution(session: Session) -> Dict[str, int]:
        """
        Retorna quantidade de transações por nível de risco.
        """
        statement = (
            select(
                Transaction.risk_level,
                func.count(Transaction.id)
            )
            .group_by(Transaction.risk_level)
        )

        results = session.exec(statement).all()

        return {risk: count for risk, count in results}

    @staticmethod
    def daily_transactions(session: Session, limit: int = 30) -> List[dict]:
        """
        Retorna volume diário de transações (para gráfico de linha).
        """
        statement = (
            select(
                func.date(Transaction.created_at).label("day"),
                func.count(Transaction.id).label("count")
            )
            .group_by(func.date(Transaction.created_at))
            .order_by(func.date(Transaction.created_at).desc())
            .limit(limit)
        )

        results = session.exec(statement).all()

        return [
            {"date": day, "count": count}
            for day, count in results
        ]

    @staticmethod
    def daily_anomalies(session: Session, limit: int = 30) -> List[dict]:
        """
        Retorna volume diário de anomalias.
        """
        statement = (
            select(
                func.date(Transaction.created_at).label("day"),
                func.count(Transaction.id).label("count")
            )
            .where(Transaction.prediction == -1)
            .group_by(func.date(Transaction.created_at))
            .order_by(func.date(Transaction.created_at).desc())
            .limit(limit)
        )

        results = session.exec(statement).all()

        return [
            {"date": day, "count": count}
            for day, count in results
        ]
