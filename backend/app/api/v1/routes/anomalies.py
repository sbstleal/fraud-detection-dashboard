from fastapi import APIRouter, HTTPException
from app.services.deteccao import detector

router = APIRouter(
    prefix="/anomalies",
    tags=["Análises"]
)


@router.get("")
def get_anomalies():
    if detector.df is None:
        raise HTTPException(
            status_code=503,
            detail="Dados ainda não carregados."
        )

    if "prediction" not in detector.df.columns:
        raise HTTPException(
            status_code=503,
            detail="Modelo ainda não executou predições."
        )

    anomalies = detector.df[detector.df["prediction"] == -1]

    return {
        "total_transactions": len(detector.df),
        "total_anomalies": len(anomalies),
        "percentage": f"{(len(anomalies) / len(detector.df)) * 100:.2f}%",
        "data": anomalies.to_dict(orient="records")
    }
