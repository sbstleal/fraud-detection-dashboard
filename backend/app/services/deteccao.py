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
        self.df = None  # <--- ADICIONADO: Variável para guardar o histórico (para a rota /anomalies)
        self.load_resources()

    def load_resources(self):
        """Carrega o Modelo e o Scaler salvos no notebook"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ajuste o caminho conforme sua estrutura real
        # Tenta voltar para backend/models
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

            # 2. Carrega o Scaler
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info(f"✅ Scaler carregado de: {scaler_path}")
            else:
                logger.error(f"❌ Scaler não encontrado em: {scaler_path}")

        except Exception as e:
            logger.error(f"❌ Erro crítico ao carregar recursos: {e}")

    def processar_csv_historico(self, filepath: str):
        """
        Lê um CSV histórico, aplica o modelo salvo e salva no self.df.
        Usado pela rota GET /anomalies e pelo Dashboard.
        """
        try:
            if not self.model or not self.scaler:
                logger.warning("⚠️ Tentativa de processar CSV sem modelo carregado.")
                return

            logger.info(f"📂 Processando histórico: {filepath}")
            df = pd.read_csv(filepath)
            
            # --- PREPARAÇÃO DOS DADOS (Mesma lógica do predict_transaction) ---
            # Nota: O scaler e o modelo esperam colunas específicas.
            # Aqui assumimos que o CSV tem 'Amount', 'Time' e as colunas V1..V28
            
            # Criamos uma cópia para não alterar o original durante os cálculos
            df_process = df.copy()

            # Aplica Scaler (Ajuste conforme o fit original do seu scaler)
            # Se o scaler foi treinado com fit_transform(df[['Amount', 'Time']]), use assim:
            # Se foi separado, mantenha a lógica. Vou assumir o padrão comum:
            if 'Amount' in df_process.columns and 'Time' in df_process.columns:
                df_process['scaled_amount'] = self.scaler.fit_transform(df_process['Amount'].values.reshape(-1, 1))
                df_process['scaled_time'] = self.scaler.fit_transform(df_process['Time'].values.reshape(-1, 1))
                df_process.drop(['Time', 'Amount'], axis=1, inplace=True, errors='ignore')

            # Garante ordem das colunas
            cols_model = self.model.feature_names_in_
            df_process = df_process[cols_model]

            # --- PREDIÇÃO EM MASSA ---
            # predict_proba retorna [[prob_0, prob_1], ...] - queremos a coluna 1 (fraude)
            probs = self.model.predict_proba(df_process)[:, 1]
            
            # Salva no DataFrame original
            df['score'] = probs
            # Regra de negócio: > 20% é fraude (-1 para manter compatibilidade ou 1)
            # Vamos usar 1 = Fraude, 0 = Normal (Padrão supervisionado)
            # Mas se seu frontend espera -1 para anomalia, descomente a linha abaixo:
            # df['prediction'] = np.where(probs >= 0.20, -1, 1) 
            
            df['prediction'] = np.where(probs >= 0.20, -1, 1) # Usando -1 para anomalia (compatível com rota anterior)

            self.df = df # Guarda na memória
            logger.info(f"✅ Histórico processado. Anomalias encontradas: {len(df[df['prediction'] == -1])}")

        except Exception as e:
            logger.error(f"❌ Erro ao processar CSV histórico: {e}")

    def predict_transaction(self, features: dict):
        """
        Faz a previsão de uma única transação (para endpoint POST).
        """
        if not self.model or not self.scaler:
            return {"error": "Servidor iniciou mas o Modelo/Scaler não foram carregados."}

        try:
            df_input = pd.DataFrame([features])
            
            if 'Amount' not in df_input.columns or 'Time' not in df_input.columns:
                return {"error": "Campos 'Amount' e 'Time' são obrigatórios."}

            # Lógica do Scaler (Exatamente como você enviou)
            amount_val = df_input['Amount'].values.reshape(-1, 1)
            time_val = df_input['Time'].values.reshape(-1, 1)

            df_input['scaled_amount'] = self.scaler.transform(amount_val)
            df_input['scaled_time'] = self.scaler.transform(time_val)

            df_input.drop(['Time', 'Amount'], axis=1, inplace=True)

            cols_model = self.model.feature_names_in_
            df_input = df_input[cols_model]

            probabilidade = self.model.predict_proba(df_input)[0][1]
            
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

# Instância global
detector = FraudDetector()