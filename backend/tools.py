# Módulo Definidor de Tools e Schema de Agentes

def get_github_status(username: str) -> dict:
    """
    Busca métricas e status profissional do perfil do GitHub de um desenvolvedor alvo para ver a atividade recente.
    """
    return {
        "username": username,
        "public_repos": 45,
        "open_source_contributions": "Constantes",
        "recent_activity": "Construindo RAGs e Agentes em LangGraph/FastAPI",
        "work_status": "Disponível para recolocação na área de Inteligência Artificial"
    }

def get_tech_stack_summary(focus_area: str) -> str:
    """
    Retorna uma visão sumarizada das tecnologias e habilidades técnicas baseada no contexto ou vaga que o recrutador quer preencher.
    """
    focus_area = str(focus_area).lower()
    
    if "backend" in focus_area or "api" in focus_area or "python" in focus_area:
        return "Especialidade Backend: Domínio profundo de Python, FastAPI (roteamento seguro, dependency injection) e Pydantic para validação robusta."
    elif "ia" in focus_area or "agent" in focus_area or "rag" in focus_area or "llm" in focus_area:
        return "Especialidade em IA: Arquitetura RAG avançada, Tool Use fluído direto via APIs base, orquestração de Agentes usando LangGraph e PydanticAI."
    else:
        return "Core Stack: Transição eficiente do ecossistema geral da Ecolabora para IA com Python, FastAPI e Streamlit como frontends de demonstração."

# JSON SCHEMA exigido pela documentação oficial da Anthropic API para Tool Use / Function Calling
AGENT_TOOLS = [
    {
        "name": "get_github_status",
        "description": "Busca métricas e status profissional do perfil do GitHub de um desenvolvedor alvo para ver a atividade recente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "O handle/nome de usuário no GitHub."
                }
            },
            "required": ["username"]
        }
    },
    {
        "name": "get_tech_stack_summary",
        "description": "Retorna uma visão sumarizada das tecnologias e habilidades técnicas baseada no contexto ou vaga que o recrutador quer preencher.",
        "input_schema": {
            "type": "object",
            "properties": {
                "focus_area": {
                    "type": "string",
                    "description": "A especialidade/área de foco requerida (Exemplos possíveis: 'IA', 'Backend', 'Data', 'APIs')."
                }
            },
            "required": ["focus_area"]
        }
    }
]
