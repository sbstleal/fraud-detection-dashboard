import sys
import os

# --- CORREÇÃO DE IMPORTAÇÃO ---
# Pega o caminho absoluto da pasta onde este arquivo (seed_data.py) está
current_dir = os.path.dirname(os.path.abspath(__file__))
# Adiciona esse caminho à lista de busca do Python
sys.path.append(current_dir)
# ------------------------------

import pandas as pd
from sqlmodel import Session, select

# Agora tenta importar o backend
try:
    from backend.app.core.database import engine, create_db_and_tables
    from backend.models import Transaction
    print("✅ Módulos do backend importados com sucesso!")
except ImportError as e:
    print("\n❌ ERRO CRÍTICO DE IMPORTAÇÃO")
    print(f"O Python não encontrou o módulo: {e}")
    print("Verifique se o arquivo '__init__.py' existe dentro da pasta 'backend'.")
    sys.exit(1)

# ... (O resto do código continua igual: CSV_FILE_PATH = ...)