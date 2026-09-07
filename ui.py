import streamlit as st
from chatbot import chatbot_api

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
        # Call chatbot directly (no backend server needed)
        try:
            answer = chatbot_api(suggestion)
        except Exception as e:
            answer = f"⚠️ Error: {e}"
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

    # Call chatbot directly (no backend server needed)
    try:
        answer = chatbot_api(user_input)
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    # Assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    with st.chat_message("assistant"):
        st.markdown(answer)
