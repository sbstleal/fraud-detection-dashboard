from pathlib import Path
import logging

import joblib
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class FraudDetector:
    """
    Serviço responsável por aplicar o modelo de detecção de fraude
    em DataFrames de transações.

    Funciona com modelo real ou em modo fallback (sem ML).
    """

    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        base_dir = Path(__file__).resolve().parents[2]
        models_dir = base_dir / "models"

        model_path = models_dir / "random_forest_v1.pkl"
        scaler_path = models_dir / "scaler_v1.pkl"

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

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica o modelo (ou fallback) em um DataFrame de transações.

        Retorna o mesmo DataFrame com:
        - prediction
        - risk_score
        - risk_level
        """

        df = df.copy()

        # Normaliza nomes
        df.columns = [c.lower() for c in df.columns]

        # ==========================
        # Fallback (sem ML)
        # ==========================
        if self.model is None or self.scaler is None:
            logger.warning("⚠️ Executando detector em modo fallback (sem ML).")

            df["risk_score"] = np.clip(df["amount"] / 5000, 0, 1)
            df["prediction"] = np.where(df["risk_score"] >= 0.7, -1, 1)

        # ==========================
        # Modelo real
        # ==========================
        else:
            features = df.drop(columns=["class"], errors="ignore")

            if "amount" in features.columns:
                features["scaled_amount"] = self.scaler.transform(
                    features["amount"].values.reshape(-1, 1)
                )
                features.drop(columns=["amount"], inplace=True)

            if "time" in features.columns:
                features["scaled_time"] = self.scaler.transform(
                    features["time"].values.reshape(-1, 1)
                )
                features.drop(columns=["time"], inplace=True)

            features = features[self.model.feature_names_in_]

            probs = self.model.predict_proba(features)[:, 1]

            df["risk_score"] = probs
            df["prediction"] = np.where(probs >= 0.20, -1, 1)

        # ==========================
        # Risk level
        # ==========================
        df["risk_level"] = pd.cut(
            df["risk_score"],
            bins=[-0.01, 0.3, 0.7, 1.0],
            labels=["LOW", "MEDIUM", "HIGH"]
        )

        return df

    def predict_transaction(self, features: dict) -> dict:
        """
        Predição unitária (endpoint POST).
        """

        df = pd.DataFrame([features])
        df = self.process_dataframe(df)

        return {
            "prediction": int(df.iloc[0]["prediction"]),
            "risk_score": float(df.iloc[0]["risk_score"]),
            "risk_level": df.iloc[0]["risk_level"]
        }


# Instância global
detector = FraudDetector()