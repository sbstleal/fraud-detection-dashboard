from pydantic import BaseModel, Field
from typing import Dict

class TransactionInput(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Variáveis da transação (Time, Amount, V1 até V28)",
        min_items=30,
        example={
            "Time": 1000.0,
            "Amount": 150.50,
            "V1": -1.3598,
            "V2": -0.0727,
            "V3": 2.5363,
            "V4": 1.3781
        }
    )

class PredictionResponse(BaseModel):
    is_fraud: bool = Field(..., description="Indica se a transação é fraudulenta")
    probability: float = Field(
        ..., ge=0, le=1, description="Probabilidade estimada de fraude"
    )
    risk_level: str = Field(
        ..., description="Nível de risco: baixo, médio ou alto"
    )
    message: str = Field(..., description="Mensagem explicativa do resultado")
