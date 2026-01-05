from pydantic import BaseModel
from typing import Dict, List


class GlobalKPIsResponse(BaseModel):
    total_transactions: int
    total_anomalies: int
    anomaly_rate: float


class RiskDistributionResponse(BaseModel):
    distribution: Dict[str, int]


class DailyMetric(BaseModel):
    date: str
    count: int


class DailyMetricsResponse(BaseModel):
    data: List[DailyMetric]