from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.kpi_repository import KPIRepository

router = APIRouter(
    prefix="/kpis",
    tags=["KPIs"]
)


@router.get("/overview")
def kpis_overview(
    session: Session = Depends(get_session)
):
    """
    KPIs principais do sistema (cards do dashboard).
    """
    total = KPIRepository.total_transactions(session)
    anomalies = KPIRepository.total_anomalies(session)

    return {
        "total_transactions": total,
        "total_anomalies": anomalies,
        "anomaly_rate": KPIRepository.anomaly_rate(session)
    }


@router.get("/risk-distribution")
def risk_distribution(
    session: Session = Depends(get_session)
):
    """
    Distribuição de transações por nível de risco.
    """
    return KPIRepository.risk_distribution(session)


@router.get("/daily-transactions")
def daily_transactions(
    limit: int = 30,
    session: Session = Depends(get_session)
):
    """
    Volume diário de transações.
    """
    return KPIRepository.daily_transactions(session, limit)


@router.get("/daily-anomalies")
def daily_anomalies(
    limit: int = 30,
    session: Session = Depends(get_session)
):
    """
    Volume diário de anomalias.
    """
    return KPIRepository.daily_anomalies(session, limit)
