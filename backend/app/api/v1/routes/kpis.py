from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.kpi_repository import KPIRepository

router = APIRouter(
    prefix="/kpis",
    tags=["KPIs"]
)
