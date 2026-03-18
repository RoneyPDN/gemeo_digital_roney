import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Roney AI",
    page_icon="✨",
    layout="wide" # Use wide layout to mock Gemini/ChatGPT better
)

# Custom CSS for Gemini/ChatGPT-like UI
st.markdown("""
<style>
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Content styling */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 850px !important;
    }
    
    /* Make Title smaller and cleaner */
    h1 {
        text-align: center;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 2rem !important;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
    }

    /* Style the Chat Messages to look like ChatGPT/Gemini */
    [data-testid="stChatMessage"] {
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Assistant Message */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #f7f7f8 !important; /* light gray like ChatGPT */
        border: none !important;
    }
    
    /* Dark mode adjustments for Assistant Message */
    @media (prefers-color-scheme: dark) {
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #444654 !important; /* dark gray like ChatGPT */
        }
    }

    /* Input Box */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid #d1d5db !important;
    }
</style>
""", unsafe_allow_html=True)

def format_history_for_api(messages: list) -> list:
    history = []
    for msg in messages:
        if "role" in msg and "content" in msg:
            history.append({"role": msg["role"], "content": msg["content"]})
    return history

def check_login():
    """Retorna True se o usuário e senha estiverem corretos."""
    if "login_sucesso" not in st.session_state:
        st.session_state["login_sucesso"] = False

    if not st.session_state["login_sucesso"]:
        st.markdown("### 🔒 Acesso Restrito")
        st.markdown("Por favor, insira as credenciais para acessar o Gêmeo Digital.")
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                if username.strip().lower() == "empresa" and password == "3007":
                    st.session_state["login_sucesso"] = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        return False
    return True

if check_login():
    st.title("✨ Gêmeo Digital do Roney")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Eu sou o assistente virtual do **Roney Pereira**. Fui instruído com os dados da sua carreira, portfólio e habilidades técnicas. Estou aqui para mostrar meu potencial. Como posso ajudar a sua empresa hoje?"}
        ]

    # Display Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Pergunte-me sobre a experiência do Roney ou habilidades técnicas..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Exclude the newly appended user message from the history if needed
                    # Actually, our backend takes history + current message in request
                    history_for_api = format_history_for_api(st.session_state.messages[:-1])
                        
                    response = requests.post(
                        API_URL, 
                        json={"message": prompt, "history": history_for_api}
                    )
                    
                    if response.status_code == 200:
                        reply_text = response.json().get("response", "Erro na resposta da API.")
                        st.markdown(reply_text)
                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                    else:
                        st.error(f"Erro na API Interna: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Falha de conexão: Verifique se o backend em FastAPI está rodando na porta 8000. (Execute: `uvicorn backend.main:app`)")
