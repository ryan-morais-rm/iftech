import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="IFTech 2026")
st.title("IFTech 2026 - Modelos Classicos vs LLMs em Produção")

tab_imdb, tab_llm = st.tabs(["Classificador IMDB", "Chat LLM"])

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

with tab_llm:
    st.subheader("Chat com o LLM")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Pergunte algo ao modelo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/llm/chat",
                        json={"prompt": prompt},
                        timeout=180,
                    )
                    response.raise_for_status()
                    answer = response.json()["response"]
                except requests.RequestException as exc:
                    answer = f"Erro ao chamar o backend: {exc}"
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
