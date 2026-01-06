from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

from app.models.transaction import RiskLevel


class TransactionInput(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Features da transação (time, amount, v1 até v28)",
        example={
            "time": 45000,
            "amount": 3200.5,
            "v1": -1.359807,
            "v2": -0.072781,
            "v3": 2.536346,
            "v4": 1.378155,
            "v5": -0.338321,
            "v6": 0.462388,
            "v7": 0.239599,
            "v8": 0.098698,
            "v9": 0.363787,
            "v10": 0.090794,
            "v11": -0.5516,
            "v12": -0.617801,
            "v13": -0.99139,
            "v14": -0.311169,
            "v15": 1.468177,
            "v16": -0.470401,
            "v17": 0.207971,
            "v18": 0.025791,
            "v19": 0.403993,
            "v20": 0.251412,
            "v21": -0.018307,
            "v22": 0.277838,
            "v23": -0.110474,
            "v24": 0.066928,
            "v25": 0.128539,
            "v26": -0.189115,
            "v27": 0.133558,
            "v28": -0.021053,
        },
    )


class PredictionResponse(BaseModel):
    is_fraud: bool
    probability: float = Field(..., ge=0, le=1)
    risk_level: str
    message: str

class TransactionRead(BaseModel):
    id: int
    time: float
    amount: float

    v1: float
    v2: float
    v3: float
    v4: float
    v5: float
    v6: float
    v7: float
    v8: float
    v9: float
    v10: float
    v11: float
    v12: float
    v13: float
    v14: float
    v15: float
    v16: float
    v17: float
    v18: float
    v19: float
    v20: float
    v21: float
    v22: float
    v23: float
    v24: float
    v25: float
    v26: float
    v27: float
    v28: float

    prediction: int
    risk_score: Optional[float]
    risk_level: Optional[RiskLevel]
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedTransactionsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TransactionRead]

class TransactionFilter(BaseModel):
    is_fraud: Optional[bool] = None

    risk_level: Optional[RiskLevel] = None
    min_risk_score: Optional[float] = Field(None, ge=0, le=1)
    max_risk_score: Optional[float] = Field(None, ge=0, le=1)

    min_amount: Optional[float] = None
    max_amount: Optional[float] = None