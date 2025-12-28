from fastapi import FastAPI

app = FastAPI(
    title="API de Deteccção de Fraudes",
    description="API para detecção de fraudes em transações financeiras utilizando modelos de machine learning.",
    version="1.0.0",
)

@app.get("/status")
def status_api():
    return {
        "status": "online",
        "servico": "detecção de fraudes"
    }