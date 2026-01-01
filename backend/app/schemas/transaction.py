from pydantic import BaseModel, Field
from typing import Dict

# 1. O que a API DEVOLVE para o usuário (Output)
class PredictionResponse(BaseModel):
    is_fraud: bool
    probability: float
    risk_level: str
    message: str

# 2. O que a API RECEBE do usuário (Input)
class TransactionInput(BaseModel):
    features: Dict[str, float] = Field(
        ..., 
        description="Dicionário contendo as 30 variáveis (Time, Amount, V1..V28)",
        example={
            "Time": 1000.0,
            "Amount": 150.50,
            "V1": -1.3598, "V2": -0.0727, "V3": 2.5363, "V4": 1.3781
        }
    )
