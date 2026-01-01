from fastapi import FastAPI, HTTPException
from app.services.deteccao import detector
from app.schemas.transaction import TransactionInput, PredictionResponse

app = FastAPI(
    title="API de Detecção de Fraudes",
    description="API que utiliza Random Forest para identificar transações suspeitas em tempo real.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Rota de verificação de saúde da API."""
    return {
        "status": "online", 
        "message": "Bem-vindo ao Detector de Fraudes 🕵️‍♂️",
        "model_loaded": detector.model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: TransactionInput):
    """
    Analisa uma transação financeira.
    
    - **Recebe**: Um dicionário de features (Time, Amount, V1-V28).
    - **Retorna**: Probabilidade de fraude e decisão (Bloquear/Aprovar).
    """
    
    # O Pydantic já garantiu que 'request.features' existe e é um dicionário
    features = request.features
    
    # Chama o serviço (Cérebro)
    result = detector.predict_transaction(features)
    
    # Se houve erro interno no serviço (ex: modelo não carregou)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result