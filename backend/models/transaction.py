from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Transaction(SQLModel, table=True):
    """
    Este modelo define a TABELA 'transaction' no PostgreSQL.
    Diferente do Schema da API, aqui definimos colunas físicas.
    """
    
    # Identificador único no banco (Primary Key)
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Data de criação do registro no banco (Auditoria)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Dados Financeiros
    time: float = Field(alias="Time")
    amount: float = Field(alias="Amount")
    
    # Classificação: 0 (Normal) ou 1 (Fraude)
    # class_id é necessário pois 'class' é palavra reservada no Python
    class_id: int = Field(alias="Class")

    # --- Features do PCA (V1 a V28) ---
    # No banco, criamos uma coluna para cada feature para permitir queries rápidas.
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

    class Config:
        # Permite popular o modelo usando chaves "Time" ou "Class" (igual ao CSV)
        populate_by_name = True