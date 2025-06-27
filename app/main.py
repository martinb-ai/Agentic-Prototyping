import streamlit as st
from openai import OpenAI
from agents import get_triage_agent
from tools import get_tools
from data import load_data
from config import AppConfig

# --- App Configuration ---
st.set_page_config(
    page_title="Agentic Workshop Chat",
    page_icon="🤖",
    layout="wide"
)

# --- State Management ---
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'triage_agent' not in st.session_state:
    st.session_state.triage_agent = get_triage_agent()

# --- UI ---
st.title("🤖 Agentic Workshop Chat")
st.sidebar.header("Configuration")

# --- Main Chat Interface ---
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # This is a simplified example of how you might run the agent.
        # In a real application, you would use the Runner from the openai-agents SDK
        # and handle the full conversational state.
        # For this example, we'll just get a direct response.
        client = OpenAI()
        response = client.chat.completions.create(
            model=AppConfig.DEFAULT_MODEL,
            messages=[
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.conversation
            ],
            stream=True,
        )
        for chunk in response:
            full_response += (chunk.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.conversation.append({"role": "assistant", "content": full_response})
