import streamlit as st
import requests

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Groundwater AI Chatbot",
    page_icon="💧",
    layout="centered"
)

st.title("💧 Groundwater AI Chatbot")
st.caption("INGRES-based Hybrid AI System (CSV + FAISS + LLM)")

# ===============================
# Initialize chat history
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# Suggested Queries
# ===============================
SUGGESTIONS = [
    "How many states are over exploited in 2019?",
    "Which blocks are semi critical in 2020?",
    "Explain groundwater condition of Bihar in 2020",
    "Why is groundwater over-exploitation a concern?",
    "Describe groundwater status of Hoskote block in 2019"
]

st.markdown("### 🔍 Try asking:")
cols = st.columns(len(SUGGESTIONS))

for i, suggestion in enumerate(SUGGESTIONS):
    if cols[i].button(suggestion):
        # Add user message
        st.session_state.messages.append(
            {"role": "user", "content": suggestion}
        )

        # Call backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"query": suggestion},
                timeout=60
            )
            answer = response.json().get("answer", "No response received.")
        except Exception as e:
            answer = f"⚠️ Backend error: {e}"

        # Add assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

# ===============================
# Display chat history
# ===============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# Chat Input (ChatGPT-style)
# ===============================
user_input = st.chat_input("Ask anything about groundwater...")

if user_input:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Backend call
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"query": user_input},
            timeout=60
        )
        answer = response.json().get("answer", "No response received.")
    except Exception as e:
        answer = f"⚠️ Backend error: {e}"

    # Assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    with st.chat_message("assistant"):
        st.markdown(answer)
