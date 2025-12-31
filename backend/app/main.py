from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
# Aqui importamos a lógica de IA que criamos na etapa anterior
from app.services.deteccao import detector 

app = FastAPI(
    title="API de Detecção de Fraudes",
    description="API para detecção de anomalias em transações financeiras.",
    version="1.0.0",
)

# 1. Modelo de Validação (Pydantic)
# Define que o usuário TEM que enviar um JSON com "features"
class TransactionData(BaseModel):
    # Ex: {"V1": 0.12, "V2": -4.5 ... "Amount": 100.0}
    features: Dict[str, float]

# 2. Rota de Status (Mantivemos a sua, apenas padronizei o retorno)
@app.get("/status")
def status_api():
    return {
        "status": "online",
        "service": "Fraud Detection v1",
        "model_loaded": detector.model is not None # Mostra se o modelo carregou
    }

# 3. Rota de Predição (A NOVIDADE)
@app.post("/predict")
def predict(data: TransactionData):
    try:
        # Chama a função que criamos no arquivo deteccao.py
        result = detector.predict_transaction(data.features)
        
        if "error" in result:
            raise HTTPException(status_code=503, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))