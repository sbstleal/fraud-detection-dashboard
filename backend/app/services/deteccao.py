import joblib
import pandas as pd
import os
import logging
import numpy as np

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudDetector:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_resources()

    def load_resources(self):
        """Carrega o Modelo e o Scaler salvos no notebook"""
        # Pega a pasta onde este arquivo deteccao.py está
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Sobe duas pastas (services -> app -> backend) e entra em 'models'
        # Caminho final esperado: backend/models/
        models_dir = os.path.abspath(os.path.join(base_dir, "../../models"))
        
        model_path = os.path.join(models_dir, "random_forest_v1.pkl")
        scaler_path = os.path.join(models_dir, "scaler_v1.pkl")
        
        try:
            # 1. Carrega o Modelo
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"✅ Modelo carregado de: {model_path}")
            else:
                logger.error(f"❌ Modelo não encontrado em: {model_path}")

            # 2. Carrega o Scaler (Fundamental para Random Forest)
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info(f"✅ Scaler carregado de: {scaler_path}")
            else:
                logger.error(f"❌ Scaler não encontrado em: {scaler_path}")

        except Exception as e:
            logger.error(f"❌ Erro crítico ao carregar recursos: {e}")

    def predict_transaction(self, features: dict):
        """
        Recebe os dados brutos, aplica o Scaler e faz a previsão.
        """
        if not self.model or not self.scaler:
            return {"error": "Servidor iniciou mas o Modelo/Scaler não foram carregados. Verifique a pasta 'models'."}

        try:
            # A. Converte dicionário para DataFrame
            df_input = pd.DataFrame([features])
            
            # Validação básica
            if 'Amount' not in df_input.columns or 'Time' not in df_input.columns:
                return {"error": "Os campos 'Amount' e 'Time' são obrigatórios no JSON."}

            # B. APLICA O SCALER (Exatamente como no Notebook)
            # O modelo aprendeu com 'scaled_amount' e 'scaled_time', não com os valores originais
            amount_val = df_input['Amount'].values.reshape(-1, 1)
            time_val = df_input['Time'].values.reshape(-1, 1)

            df_input['scaled_amount'] = self.scaler.transform(amount_val)
            df_input['scaled_time'] = self.scaler.transform(time_val)

            # Remove colunas originais
            df_input.drop(['Time', 'Amount'], axis=1, inplace=True)

            # C. GARANTE A ORDEM DAS COLUNAS
            # Se o JSON vier bagunçado (V2 antes de V1), isso arruma
            cols_model = self.model.feature_names_in_
            df_input = df_input[cols_model]

            # D. PREVISÃO COM PROBABILIDADE
            # Pega a chance de ser classe 1 (Fraude)
            probabilidade = self.model.predict_proba(df_input)[0][1]
            
            # E. REGRA DE NEGÓCIO (Limiar de 20%)
            # Definimos no notebook que acima de 20% já é risco
            limiar = 0.20 
            is_fraud = probabilidade >= limiar
            
            return {
                "is_fraud": bool(is_fraud),
                "probability": float(probabilidade),
                "risk_level": "ALTO" if is_fraud else "BAIXO",
                "message": "BLOQUEAR TRANSAÇÃO" if is_fraud else "APROVADA"
            }

        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}")
            return {"error": str(e)}

# Instância global para ser importada no main.py
detector = FraudDetector()