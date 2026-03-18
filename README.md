# Projeto: O Gêmeo Digital do Roney 🤖

Este é um projeto de demonstração para processo seletivo de **AI Engineer Senior**. Ele exemplifica a construção de um Agente Baseado em LLM utilizando RAG e Tool Use através de código limpo e bibliotecas consolidadas.

## 🚀 Tecnologias Utilizadas
- **Backend:** FastAPI, Python, Pydantic
- **Frontend:** Streamlit
- **Inteligência Artificial:** Claude 3.5 Sonnet (Anthropic API)
- **Técnicas Empregadas:**
  - **RAG (Retrieval-Augmented Generation):** Carregamento de contexto profissional a partir de arquivo local.
  - **Function Calling (Tool Use):** O Agente é capaz de invocar ferramentas Python para recuperar dados dinâmicos (Ex: Resumo de Tech Stack, GitHub Info).

## 📁 Estrutura do Projeto
```
gemeo_digital_roney/
├── backend/
│   ├── data/
│   │   └── roney_profile.md
│   ├── agent.py
│   ├── main.py
│   └── tools.py
├── frontend/
│   └── app.py
├── .env.example
├── README.md
└── requirements.txt
```

## 🛠️ Como Executar

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**2. Configure a API Key:**
Crie um arquivo `.env` na raiz do projeto copiando o `.env.example` e adicione sua chave de API da Anthropic.
`ANTHROPIC_API_KEY=sua_chave`

**3. Inicie o Servidor Backend (FastAPI):**
Abra um terminal na raiz do projeto e rode:
```bash
uvicorn backend.main:app --reload --port 8000
```
Isso fará a API rodar em `http://localhost:8000`.

**4. Inicie o Frontend (Streamlit):**
Abra um segundo terminal na raiz do projeto e rode:
```bash
streamlit run frontend/app.py
```
A interface web será aberta no seu navegador sem bloqueios, simulando uma interface de chat moderna semelhante ao ChatGPT/Gemini.
