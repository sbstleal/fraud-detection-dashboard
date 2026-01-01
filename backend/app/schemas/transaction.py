from pydantic import BaseModel, Field
from typing import Dict

<<<<<<< HEAD
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
=======
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
>>>>>>> temp-salvacao
