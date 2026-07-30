import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="IFTech 2026")
st.title("IFTech 2026 - Modelos Classicos vs LLMs em Produção")

tab_imdb, tab_llm_local, tab_llm_api = st.tabs(
    ["Classificador IMDB", "Chat LLM Local", "Chat LLM API"]
)

with tab_imdb:
    st.subheader("Analise de Sentimento")
    review = st.text_area("Digite uma resenha de filme (em ingles):")

    if st.button("Classificar"):
        if not review.strip():
            st.warning("Digite um texto antes de classificar.")
        else:
            with st.spinner("Classificando..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/classifier/predict",
                        json={"text": review},
                        timeout=30,
                    )
                    response.raise_for_status()
                    data = response.json()
                    emoji = "😀" if data["sentiment"] == "Positivo" else "😞"
                    st.success(
                        f"Sentimento: **{data['sentiment']}** {emoji} "
                        f"(confianca: {data['confidence']:.0%})"
                    )
                except requests.RequestException as exc:
                    st.error(f"Erro ao chamar o backend: {exc}")

def render_chat_tab(endpoint: str, session_key: str):
    if session_key not in st.session_state:
        st.session_state[session_key] = []

    chat_box = st.container(height=500)

    for message in st.session_state[session_key]:
        with chat_box.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Pergunte algo ao modelo...", key=f"input_{session_key}"):
        st.session_state[session_key].append({"role": "user", "content": prompt})
        with chat_box.chat_message("user"):
            st.markdown(prompt)

        with chat_box.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}{endpoint}",
                        json={"prompt": prompt},
                        timeout=180,
                    )
                    response.raise_for_status()
                    answer = response.json()["response"]
                except requests.RequestException as exc:
                    detail = None
                    if exc.response is not None:
                        try:
                            detail = exc.response.json().get("detail")
                        except ValueError:
                            pass
                    answer = detail or f"Erro ao chamar o backend: {exc}"
                st.markdown(answer)

        st.session_state[session_key].append({"role": "assistant", "content": answer})


with tab_llm_local:
    st.subheader("Chat com o LLM (Ollama local)")
    render_chat_tab("/llm/chat", "messages_local")

with tab_llm_api:
    st.subheader("Chat com o LLM (API)")
    render_chat_tab("/llm/chat/api", "messages_api")
