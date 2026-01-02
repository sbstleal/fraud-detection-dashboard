from typing import Optional
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Transaction(SQLModel, table=True):
    """
    Entidade central do sistema de detecção de fraudes.

    Representa uma transação financeira processada pelo modelo
    de Machine Learning, contendo:
    - features originais
    - resultado da predição
    - score e nível de risco
    """

    __tablename__ = "transactions"

    # --- IDENTIFICAÇÃO ---
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- FEATURES PRINCIPAIS ---
    time: float = Field(description="Tempo da transação em segundos")
    amount: float = Field(description="Valor da transação")

    # --- FEATURES ANONIMIZADAS (PCA: V1 a V28) ---
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

    # --- RESULTADO DO MODELO ---
    prediction: int = Field(
        description="Resultado do modelo (-1 = anomalia, 1 = normal)",
        index=True
    )

    risk_score: Optional[float] = Field(
        default=None,
        description="Score de risco da transação (0–1)"
    )

    risk_level: Optional[RiskLevel] = Field(
        default=None,
        description="Nível de risco calculado",
        index=True
    )

    # --- METADADOS ---
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data de inserção no sistema"
    )