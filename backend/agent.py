import os
import json
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from .tools import AGENT_TOOLS, get_github_status, get_tech_stack_summary

load_dotenv()

try:
    CLIENT = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "dummy_key"))
except Exception:
    CLIENT = None

MODEL_NAME = "claude-sonnet-4-20250514"

def load_rag_context() -> str:
    file_path = Path(__file__).parent / "data" / "roney_profile.md"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

SYSTEM_PROMPT = f"""
Você é o Gêmeo Digital do Roney Pereira, um Engenheiro de IA Sênior e Software Developer Full-Stack (com forte veia construtora).
O seu tom de voz é de um brasileiro nativo (Embu-Guaçu/SP), otimista, profundamente ético (cristão), extremamente grato pela sua trajetória (e por sua família) e focado em apresentar soluções.

Seu Objetivo é demonstrar para a vaga aplicada seu alto gabarito técnico (transição natural para IA vinda de fundamentos robustos) e as suas soft-skills raras no mercado.

<contexto_rag>
{{context}}
</contexto_rag>

Regras de Operação:
1. Responda em Português do Brasil de forma extremamente amigável, humanizada, mas matadora no quesito corporativo e técnico.
2. Se te perguntarem sobre família ou valores, cite a gratidão ao Sr. José e Dona Maria, ou a superação e poder da resiliência, sempre linkando "como isso afeta positivamente o seu trabalho de programador (manter a calma e focar na solução)".
3. Utilize as Ferramentas (Tool Use/Function Calling) SEMPRE que for perguntado explicitamente sobre dados em tempo real do GitHub, ou caso peçam um resumo focado da sua Stack técnica dependendo do gosto do recrutador.
4. Você domina Node.js, Java e Front-end, MAS seu foco máximo agora e para o qual você é Excelente é Arquitetura de Agentes, LLM SDKs (Google/Anthropic), FastAPI, Python, LangGraph e Workflows limpos de IA. Deixe isso claro se o assunto for para a área de Tech Stack.
"""

def process_message_with_agent(user_message: str, conversation_history: list = None) -> str:
    """Orquestrador do RAG e Tool Use com modelo Claude."""
    if CLIENT is None or os.getenv("ANTHROPIC_API_KEY") is None:
         return "❌ O Gêmeo Digital precisa da ANTHROPIC_API_KEY no arquivo .env."
         
    if conversation_history is None:
        conversation_history = []
        
    context = load_rag_context()
    if not context:
        return "⚠️ Base de conhecimentos `roney_profile.md` não encontrada."
        
    sys_prompt_fmt = SYSTEM_PROMPT.replace("{context}", context)
    messages = conversation_history + [{"role": "user", "content": user_message}]
    
    try:
        response = CLIENT.messages.create(
            model=MODEL_NAME,
            max_tokens=1000,
            system=sys_prompt_fmt,
            tools=AGENT_TOOLS,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            tool_call = response.content[-1]
            tool_name = tool_call.name
            tool_input = tool_call.input
            
            if tool_name == "get_github_status":
                result = get_github_status(tool_input.get("username", "RoneyPDN"))
            elif tool_name == "get_tech_stack_summary":
                result = get_tech_stack_summary(tool_input.get("focus_area", "Geral"))
            else:
                result = "Ferramenta desconhecida."
                
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    }
                ]
            })
            
            final_response = CLIENT.messages.create(
                model=MODEL_NAME,
                max_tokens=1000,
                system=sys_prompt_fmt,
                tools=AGENT_TOOLS,
                messages=messages
            )
            return final_response.content[0].text
            
        return response.content[0].text
        
    except Exception as e:
        return f"❌ Erro Systema (Claude): {str(e)}"
