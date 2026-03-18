from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .agent import process_message_with_agent

app = FastAPI(
    title="Assistente Digital do Roney - API",
    description="API FastAPI para servir o Assistente Digital do Roney, utilizando Arquitetura RAG e Agentes (Tool Use).",
    version="1.0.0"
)

# Modelos do Pydantic para tipagem estrita de Entrada e Saída
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Assistente Digital do Roney API está rodando!"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    try:
        # Converter o histórico Pydantic para as dictionaries nativas de requisição
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in req.history] if req.history else []
        reply = process_message_with_agent(req.message, history_dicts)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
