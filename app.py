import streamlit as st
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="💬 AI Chatbot", layout="wide")
st.title("💬 AI Chatbot with Memory")
st.markdown("### Powered by Groq + LLaMA 3 — Remembers your entire conversation!")

# Sidebar
st.sidebar.header("⚙️ Settings")
system_prompt = st.sidebar.selectbox("🎭 Chatbot Personality", [
    "You are a helpful AI assistant.",
    "You are an expert AI & Data Science tutor.",
    "You are a motivational coach.",
    "You are a Python programming expert.",
    "You are a career advisor for tech students."
])
temperature = st.sidebar.slider("🌡️ Creativity", 0.0, 1.0, 0.7)
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Rohith V** | [🔗 LinkedIn](https://www.linkedin.com/in/rohithv0507/)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build messages with system prompt
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # Get response from Groq
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=1024
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
