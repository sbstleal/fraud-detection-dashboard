from fastapi import FastAPI
from datetime import datetime
from pathlib import Path
import os

from app.core.config import settings
from app.api.v1.prediction import router as prediction_router
from app.services.deteccao import detector 

# Inicializa FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para detecção de transações financeiras suspeitas.",
    version="1.0.0",
    debug=settings.DEBUG
)

# --- EVENTO DE INICIALIZAÇÃO ---
@app.on_event("startup")
def startup_event():
    """
    Roda assim que a API inicia.
    Localiza o dataset 'creditcard.csv' e carrega no detector.
    """
    print("🔄 Inicializando API e procurando dados...")

    # 1. Localiza a raiz do projeto
    # O arquivo main.py está em: .../seu-projeto/backend/app/main.py
    current_file = Path(__file__).resolve()
    
    # Sobe 3 níveis para chegar na raiz do projeto (.../seu-projeto/)
    project_root = current_file.parent.parent.parent
    
    # 2. Define o caminho exato que você pediu
    # Caminho final: .../seu-projeto/data/raw/creditcard.csv
    caminho_csv = project_root / "data" / "raw" / "creditcard.csv"

    print(f"📂 Caminho definido: {caminho_csv}")

    # 3. Verifica e carrega
    if caminho_csv.exists():
        try:
            # Converte para string para passar para o pandas/detector
            detector.processar_csv_historico(str(caminho_csv))
            
            if detector.df is not None:
                print(f"✅ Sucesso: {len(detector.df)} transações carregadas na memória.")
            else:
                print("⚠️ Aviso: O arquivo foi lido, mas o DataFrame ficou vazio.")
        except Exception as e:
            print(f"❌ Erro ao processar o CSV: {e}")
    else:
        print("❌ ERRO CRÍTICO: Arquivo 'creditcard.csv' não encontrado.")
        print(f"   O sistema esperava encontrar o arquivo aqui: {caminho_csv}")
        print("   Verifique se o nome do arquivo não está como 'creditcard.csv.txt' ou algo similar.")

# --- ROTAS ---

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de saúde da aplicação.
    """
    model_ok = detector.model is not None
    data_ok = detector.df is not None
    
    status_code = 200 if (model_ok and data_ok) else 503
    
    return {
        "status": "ok" if status_code == 200 else "unavailable",
        "service": settings.APP_NAME,
        "model_loaded": model_ok,
        "data_loaded": data_ok,
        "total_records": len(detector.df) if data_ok else 0,
        "timestamp": datetime.utcnow()
    }, status_code

# Anomalias    
@app.get("/anomalies", tags=["Análises"])
def get_anomalies():
    """
    Retorna apenas as transações marcadas como suspeitas (anomalias).
    """
    try:
        df = detector.df

        if df is None:
            return {"message": "Os dados ainda não foram carregados. Verifique os logs do servidor."}
            
        if 'prediction' not in df.columns:
             return {"message": "O modelo ainda não processou as predições."}

        # Filtro: -1 é anomalia
        transacoes_suspeitas = df[df['prediction'] == -1]

        result = transacoes_suspeitas.to_dict(orient="records")

        return {
            "total_transactions": len(df),
            "total_anomalies": len(result),
            "percentage": f"{(len(result) / len(df)) * 100:.2f}%",
            "data": result
        }

    except Exception as e:
        return {"error": f"Erro interno ao buscar anomalias: {str(e)}"}

# Inclui rotas versionadas
app.include_router(prediction_router, prefix="/api/v1")