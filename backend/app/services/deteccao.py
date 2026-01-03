from pathlib import Path
import logging
from typing import Dict

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class FraudDetector:
    """
    Serviço responsável por aplicar o modelo de detecção de fraude
    em transações financeiras.

    - Usa RandomForest + Scaler quando disponíveis
    - Opera em modo fallback quando artefatos não existem
    """

    def __init__(self) -> None:
        self.model = None
        self.scaler = None
        self._load_artifacts()

    # ======================================================
    # LOAD DE ARTEFATOS
    # ======================================================

    def _load_artifacts(self) -> None:
        """
        Carrega modelo e scaler a partir de:
        backend/app/ml/artifacts
        """

        app_dir = Path(__file__).resolve().parents[1]
        models_dir = app_dir / "ml" / "artifacts"

        model_path = models_dir / "random_forest_v1.pkl"
        scaler_path = models_dir / "scaler_v1.pkl"

        logger.info(f"📂 Procurando artefatos em: {models_dir}")

        if model_path.exists():
            self.model = joblib.load(model_path)
            logger.info(f"✅ Modelo carregado: {model_path}")
        else:
            logger.warning(f"⚠️ Modelo não encontrado: {model_path}")

        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
            logger.info(f"✅ Scaler carregado: {scaler_path}")
        else:
            logger.warning(f"⚠️ Scaler não encontrado: {scaler_path}")

    # ======================================================
    # PROCESSAMENTO
    # ======================================================

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.lower() for c in df.columns]

        # --------------------------
        # FALLBACK (SEM ML)
        # --------------------------
        if self.model is None or self.scaler is None:
            logger.warning("⚠️ Detector em modo fallback (sem ML).")

            if "amount" not in df.columns:
                raise ValueError("Campo 'amount' é obrigatório")

            df["risk_score"] = np.clip(df["amount"] / 5000, 0, 1)
            df["prediction"] = np.where(df["risk_score"] >= 0.7, -1, 1)

        # --------------------------
        # MODELO REAL
        # --------------------------
        else:
            # Validação forte
            missing = [f"v{i}" for i in range(1, 29) if f"v{i}" not in df.columns]
            if missing:
                raise ValueError(f"Features faltando: {missing}")

            features = pd.DataFrame()

            # V1..V28 exatamente como no treino
            for i in range(1, 29):
                features[f"V{i}"] = df[f"v{i}"]

            # Amount
            features["scaled_amount"] = self.scaler.transform(
                df["amount"].values.reshape(-1, 1)
            )

            # Time
            features["scaled_time"] = self.scaler.transform(
                df["time"].values.reshape(-1, 1)
            )

            # Ordem exata
            features = features[self.model.feature_names_in_]

            probs = self.model.predict_proba(features)[:, 1]

            df["risk_score"] = probs
            df["prediction"] = np.where(probs >= 0.20, -1, 1)

        # --------------------------
        # RISK LEVEL
        # --------------------------
        df["risk_level"] = pd.cut(
            df["risk_score"],
            bins=[-0.01, 0.3, 0.7, 1.0],
            labels=["LOW", "MEDIUM", "HIGH"]
        )

        return df

    # ======================================================
    # PREDIÇÃO UNITÁRIA (POST /predict)
    # ======================================================

    def predict_transaction(self, features: Dict) -> Dict:
        df = pd.DataFrame([features])
        df = self.process_dataframe(df)

        row = df.iloc[0]
        is_fraud = row["prediction"] == -1

        return {
            "is_fraud": bool(is_fraud),
            "probability": float(row["risk_score"]),
            "risk_level": row["risk_level"],
            "message": (
                "Fraude detectada"
                if is_fraud
                else "Transação legítima"
            ),
        }


# ======================================================
# SINGLETON
# ======================================================

detector = FraudDetector()