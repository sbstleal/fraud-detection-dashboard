# 🚨 Fraud Detection Dashboard

Sistema completo para **detecção de anomalias em transações financeiras** utilizando  
**Aprendizado de Máquina Não Supervisionado**, **API REST com FastAPI** e **Dashboard Web interativo**.

Projeto desenvolvido com foco **acadêmico e profissional**, aplicando conceitos de
Data Science, Engenharia de Software, Machine Learning e Visualização de Dados.

---

## 📌 Visão Geral

Fraudes financeiras representam um grande desafio para instituições bancárias e fintechs,
especialmente devido ao **alto volume de transações** e à **escassez de dados rotulados**.

Este projeto propõe uma solução baseada em **detecção de anomalias**, capaz de:
- Identificar transações suspeitas
- Gerar scores de risco
- Exibir métricas e insights em dashboards interativos
- Disponibilizar os dados via API REST

---

## 🧠 Conceitos Aplicados

- Detecção de Anomalias
- Aprendizado de Máquina Não Supervisionado
- Análise Exploratória de Dados (EDA)
- Pré-processamento e normalização
# 🚨 Fraud Detection Dashboard

Sistema para detecção de anomalias em transações financeiras com API REST (FastAPI), modelo de ML não supervisionado e dashboard web interativo.

---

## 📌 Sumário

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dataset](#dataset)
- [Como Rodar](#como-rodar)
	- [Backend (API)](#backend-api)
	- [Frontend (Dashboard)](#frontend-dashboard)
- [Endpoints Principais](#endpoints-principais)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
% Fraud Detection Dashboard — Relatório Técnico

Autores: Sebastião de Oliveira Leal
Data: 2025

---

Resumo
-----

Este repositório descreve um sistema modular para detecção de anomalias em transações financeiras. A proposta central consiste em aplicar métodos de aprendizado de máquina não supervisionado para identificar transações atípicas, disponibilizando os resultados por meio de uma API REST e visualizações interativas. Este documento apresenta o problema, a base de dados utilizada, a metodologia, os experimentos realizados, instruções de reprodutibilidade e próximas etapas de pesquisa.

Palavras-chave: detecção de anomalias, isolamento de outliers, fraud detection, FastAPI, reprodutibilidade

---

1. Introdução
----------------

Fraude em transações financeiras constitui um problema crítico para instituições financeiras e plataformas de pagamento devido às perdas econômicas e à necessidade de resposta em tempo quase-real. A detecção automática de anomalias permite priorizar investigações e reduzir falsos positivos através de scores de risco. Este projeto explora abordagens não supervisionadas adaptadas ao forte desbalanceamento presente nos dados.

2. Base de Dados
------------------

- Fonte: Credit Card Fraud Detection (Kaggle)
- Características: registros de transações com atributos anonimizados (V1..V28), `Time` e `Amount`.
- Observação: por boas práticas o dataset não está versionado no repositório; disponibilize o CSV em `data/raw/creditcard.csv`.

3. Metodologia
----------------

3.1 Pré-processamento

- Limpeza de entradas faltantes
- Normalização/standardization das variáveis contínuas
- Eventual redução dimensional via PCA para visualização

3.2 Modelos avaliados

- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM

3.3 Saída do sistema

- `is_fraud` (bool): classificação binária de anomalia
- `score` (float): medida contínua de anomalia/risco
- `risk_level` (categorical): categorização em níveis (baixo/médio/alto)

4. Experimentos e Avaliação
----------------------------

Como o problema é tratado como detecção de anomalias, a avaliação combina métricas qualitativas (inspeção visual, análise de clusters) e quantitativas quando disponíveis rótulos para validação (precision@k, ROC-AUC adaptado, F1 sobre supostos positivos). Notebooks em `notebooks/` registram scripts de EDA e experimentos reprodutíveis.

5. Reprodutibilidade
---------------------

5.1 Ambiente

- Python 3.11+
- Dependências listadas em `backend/requirements.txt`

5.2 Passos para reprodução

1. Colocar `creditcard.csv` em `data/raw/creditcard.csv`.
2. Criar e ativar ambiente virtual:

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. Executar notebooks para EDA e treinamento: abrir `notebooks/model_training.ipynb`.

5.3 Checkpoint e modelos

Modelos treinados podem ser salvos em `backend/app/models`. Para fins de reprodutibilidade, registre-se os hiperparâmetros e a semente aleatória (`random_state`) utilizada.

6. Estrutura do Repositório
---------------------------

```
fraud-detection-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── eda.ipynb
│   └── model_training.ipynb
├── frontend/
└── docs/
```

7. Endpoints (resumo)
----------------------

- `GET /status` — health-check
- `POST /predict` — recebe features e retorna `PredictionResponse` (ver `backend/app/schemas/transaction.py`)
- `GET /anomalies` — lista transações marcadas como suspeitas

8. Limitações e Trabalhos Futuros
---------------------------------

- Dependência de rótulos para avaliação objetiva
- Necessidade de testes em produção (drift, latência)
- Integração com pipelines de dados em tempo real

9. Contribuições e Contato
---------------------------

Contribuições são bem-vindas via pull request. Para contato: consulte o perfil do autor no repositório.

10. Referências
----------------

- Dal Pozzolo, A., et al. (2015). Credit Card Fraud Detection dataset — Kaggle.
- Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey.

Licença: MIT

Saída do modelo:
- `is_fraud` (bool)
- `probability` / `score` (float)
- `risk_level` (str)

Os modelos treinados são salvos em `backend/app/models`.

---

## Métricas e Visualizações

Exemplos exibidos no dashboard:

- Total de transações
- Total de transações suspeitas
- Percentual de anomalias
- Valor financeiro em risco
- Anomalias ao longo do tempo
- Visualização PCA (2D)

Notebooks incluem EDA e gráficos para análise exploratória.

---

## Próximas Evoluções

- Autenticação/Autorização (JWT)
- Upload de CSV pelo usuário
- Processamento em tempo real
- Deploy com Docker + Cloud
- Explicabilidade (SHAP / LIME)

---

## Autor e Licença

**Autor:** Sebastião de Oliveira Leal

Licença: MIT
