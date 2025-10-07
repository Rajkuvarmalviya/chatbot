from dotenv import load_dotenv
import os

import streamlit as st
from groq import Groq


load_dotenv()


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in environment.")
    return Groq(api_key=api_key)


def get_groq_response(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    client = get_groq_client()
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return completion.choices[0].message.content


st.set_page_config(page_title="Groq Chat", page_icon="🤖", layout="centered")
st.title("Groq Chat 🤖")
st.caption("Ask a question and get an answer using Groq models.")

if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts with role/content

with st.form("chat_form", clear_on_submit=False):
    prompt = st.text_area("Your question", value="", height=120, placeholder="Type your question here…")
    col1, col2 = st.columns([1, 1])
    with col1:
        model = st.selectbox(
            "Model",
            [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "llama-guard-3-8b",
            ],
            index=0,
        )
    with col2:
        submitted = st.form_submit_button("Ask")

if submitted:
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking…"):
            try:
                answer = get_groq_response(prompt.strip(), model=model)
                st.session_state.history.append({"role": "user", "content": prompt.strip()})
                st.session_state.history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.history:
    st.subheader("Conversation")
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")

st.markdown("---")
st.caption("Run with: `streamlit run main.py`")