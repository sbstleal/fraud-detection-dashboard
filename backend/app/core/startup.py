from pathlib import Path
from app.services.deteccao import detector


def carregar_dados_csv():
    """
    Localiza e carrega o dataset CSV durante o startup da aplicação.
    Usado apenas em ambiente de desenvolvimento.
    """

    print("🔄 [STARTUP] Iniciando carregamento de dados CSV...")

    # Caminho do arquivo atual: backend/app/core/startup.py
    current_file = Path(__file__).resolve()

    # Sobe até a raiz do projeto
    project_root = current_file.parent.parent.parent.parent

    # Caminho esperado do CSV
    csv_path = project_root / "data" / "raw" / "creditcard.csv"

    print(f"📂 [STARTUP] Procurando arquivo em: {csv_path}")

    if not csv_path.exists():
        print("❌ [STARTUP] Arquivo creditcard.csv NÃO encontrado.")
        print("⚠️ A aplicação irá subir sem dados carregados.")
        return

    try:
        detector.processar_csv_historico(str(csv_path))

        if detector.df is not None and not detector.df.empty:
            print(f"✅ [STARTUP] {len(detector.df)} transações carregadas com sucesso.")
        else:
            print("⚠️ [STARTUP] CSV carregado, mas DataFrame está vazio.")

    except Exception as e:
        print(f"❌ [STARTUP] Erro ao carregar CSV: {e}")
