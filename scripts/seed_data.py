"""
Seed de dados para o banco PostgreSQL.

Este script:
- Cria as tabelas do banco (se não existirem)
- Lê o dataset creditcard.csv
- Processa os dados via modelo de detecção de fraude
- Persiste as transações no banco

Execução:
    python scripts/seed_data.py

Deve ser executado a partir da raiz do projeto.
"""

from __future__ import annotations

import sys
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO DE PATH (scripts/ -> raiz do projeto)
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "backend"))
# ==========================================================

import pandas as pd
from sqlmodel import Session

from app.core.database import engine, create_db_and_tables
from app.models.transaction import Transaction
from app.services.deteccao import detector

# ==========================================================
# CONSTANTES
# ==========================================================
CSV_FILE_PATH = PROJECT_ROOT / "data" / "raw" / "creditcard.csv"
BATCH_SIZE = 5_000  # evita estouro de memória
# ==========================================================


def seed_database() -> None:
    """Executa o processo completo de seed do banco."""
    print("🔄 Iniciando seed do banco de dados...")

    if not CSV_FILE_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado em: {CSV_FILE_PATH}"
        )

    # Cria tabelas (idempotente)
    create_db_and_tables()

    # Carrega dataset
    print("📥 Carregando CSV...")
    df = pd.read_csv(CSV_FILE_PATH)

    # Processa com pipeline de ML
    print("🤖 Processando dados com modelo de detecção...")
    df = detector.process_dataframe(df)

    # Garante apenas colunas do modelo
    allowed_fields = set(Transaction.model_fields.keys())
    df = df[[col for col in df.columns if col in allowed_fields]]

    print("💾 Inserindo registros no banco...")
    with Session(engine) as session:
        buffer = []

        for _, row in df.iterrows():
            buffer.append(Transaction(**row.to_dict()))

            if len(buffer) >= BATCH_SIZE:
                session.add_all(buffer)
                session.commit()
                buffer.clear()

        if buffer:
            session.add_all(buffer)
            session.commit()

    print(f"✅ {len(df)} transações inseridas com sucesso.")


def main() -> None:
    try:
        seed_database()
    except Exception as exc:
        print("❌ Erro durante o seed do banco.")
        raise exc


if __name__ == "__main__":
    main()