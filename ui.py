import streamlit as st
from chatbot import chatbot_api

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Groundwater AI Chatbot",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Custom CSS
# ===============================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
    }
    .main-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #4FC3F7, #0288D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-header p {
        color: #9AA5B1;
        font-size: 0.95rem;
    }
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #2b3a4a;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        border-color: #0288D1;
        color: #4FC3F7;
    }
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.3rem 0.2rem;
    }
    section[data-testid="stSidebar"] {
        border-right: 1px solid #2b3a4a;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# Initialize chat history
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# Sidebar
# ===============================
with st.sidebar:
    st.markdown("## 💧 Groundwater AI")
    st.caption("INGRES-based Hybrid AI System")
    st.markdown("CSV data + FAISS retrieval + Gemini LLM, combined to answer groundwater questions across Indian states and blocks.")

    st.divider()

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 🔍 Try asking")
    SUGGESTIONS = [
        "How many states are over exploited in 2019?",
        "Which blocks are semi critical in 2020?",
        "Explain groundwater condition of Bihar in 2020",
        "Why is groundwater over-exploitation a concern?",
        "Describe groundwater status of Hoskote block in 2019"
    ]
    for suggestion in SUGGESTIONS:
        if st.button(suggestion, use_container_width=True, key=f"sugg_{suggestion}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            try:
                answer = chatbot_api(suggestion, chat_history=st.session_state.messages[:-1])
            except Exception as e:
                answer = f"⚠️ Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    st.divider()
    st.caption("Data: INGRES groundwater assessment")

# ===============================
# Header
# ===============================
st.markdown("""
<div class="main-header">
    <h1>💧 Groundwater AI Chatbot</h1>
    <p>Ask about rainfall, recharge, extraction and category status across states &amp; blocks</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# Empty state
# ===============================
if not st.session_state.messages:
    st.info("👋 Start by typing a question below, or pick a suggestion from the sidebar.")

# ===============================
# Display chat history
# ===============================
for msg in st.session_state.messages:
    avatar = "💧" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ===============================
# Chat Input
# ===============================
user_input = st.chat_input("Ask anything about groundwater...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="💧"):
        with st.spinner("Thinking..."):
            try:
                answer = chatbot_api(user_input, chat_history=st.session_state.messages[:-1])
            except Exception as e:
                answer = f"⚠️ Error: {e}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
