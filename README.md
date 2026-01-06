# 🚨 Fraud Detection Dashboard

Sistema completo para detecção de anomalias em transações financeiras utilizando
Aprendizado de Máquina Não Supervisionado, API REST com FastAPI e Dashboard Web interativo.

Projeto desenvolvido com foco acadêmico e profissional, aplicando conceitos de
Data Science, Engenharia de Software, Machine Learning e Visualização de Dados.

---

## 📌 Visão Geral

Fraudes financeiras representam um grande desafio para instituições bancárias e fintechs,
especialmente devido ao alto volume de transações e à escassez de dados rotulados.

Este projeto propõe uma solução baseada em detecção de anomalias, capaz de:

- Identificar transações suspeitas
- Gerar scores de risco
- Classificar níveis de risco (LOW | MEDIUM | HIGH)
- Persistir dados em banco relacional
- Expor métricas via API REST
- Suportar dashboards analíticos

---

## 🧠 Conceitos Aplicados

- Detecção de Anomalias
- Aprendizado de Máquina Não Supervisionado
- Análise Exploratória de Dados (EDA)
- Pré-processamento e normalização
- Arquitetura de APIs REST
- Persistência de dados
- Paginação e filtros avançados

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL
- Scikit-learn
- Pandas / NumPy
- Uvicorn
- Docker (em evolução)

## 🚀 Como Rodar o Backend (API)

### 1️⃣ Criar ambiente virtual

cd backend  
python -m venv .venv  

Ative o ambiente virtual:

Windows  
.venv\Scripts\activate  

Linux / Mac  
source .venv/bin/activate  

---

### 2️⃣ Instalar dependências

pip install -r requirements.txt  

---

### 3️⃣ Subir a API

uvicorn app.main:app --reload  

---

### Acessar a documentação

Swagger UI  
http://localhost:8000/docs

## 🔌 Endpoints Principais

### 🔹 Predição

POST /api/v1/predict

Analisa uma transação financeira, persiste no banco e retorna:

- is_fraud (bool)
- probability (float)
- risk_level (LOW | MEDIUM | HIGH)
- message (string)

---

### 🔹 Transações

GET /api/v1/transactions

Lista transações com paginação e filtros:

- is_fraud
- risk_level
- min_risk_score
- max_risk_score
- min_amount
- max_amount
- limit
- offset

---

### 🔹 KPIs

GET /api/v1/kpis/overview  
GET /api/v1/kpis/risk-distribution  
GET /api/v1/kpis/daily-transactions  
GET /api/v1/kpis/daily-anomalies  

---

## 📈 Métricas Disponíveis

- Total de transações
- Total de fraudes detectadas
- Taxa de anomalias
- Distribuição por nível de risco
- Evolução diária de transações
- Evolução diária de fraudes
- Valor financeiro em risco

---

## 🤖 Modelo de Machine Learning

- Abordagem: Não supervisionada
- Features:
  - Time
  - Amount
  - V1 a V28
- Saídas:
  - Score de risco
  - Classificação de anomalia
  - Nível de risco

Os modelos treinados são armazenados em:

backend/app/ml/artifacts

## 📂 Estrutura do Projeto

fraud-detection-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── data/
├── notebooks/
├── frontend/
└── docs/

---

## ⚠️ Limitações

- Modelos não supervisionados não fornecem explicações diretas
- Sensível à distribuição dos dados
- Necessita monitoramento de data drift em produção

---

## 🔮 Próximas Evoluções

- Autenticação e autorização (JWT)
- Upload de CSV via API
- Processamento em tempo real (streaming)
- Docker e Docker Compose
- Deploy em cloud
- Explicabilidade (SHAP / LIME)

---

## 👤 Autor

Sebastião de Oliveira Leal

Projeto acadêmico e profissional focado em:

- Detecção de Fraudes
- APIs de Machine Learning
- Arquitetura de sistemas analíticos
- Engenharia de Dados

---

## 📄 Licença

MIT License
