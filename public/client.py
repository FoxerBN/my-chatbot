import streamlit as st
import time
import random
import requests
API_URL = "http://127.0.0.1:5000/ai"
st.set_page_config(page_title="Richard Chat", page_icon="💬", layout="wide")


if "messages" not in st.session_state:
    try:
        res = requests.get(f"{API_URL}/fetch_chat")
        if res.status_code == 200:
            data = res.json()
            st.session_state.messages = data.get("messages", [])
            if not st.session_state.messages:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Hi, I’m Richard 👋 — how can I help you today?"}
                ]
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi, I’m Richard 👋 — how can I help you today?"}
            ]
    except Exception as e:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I’m Richard 👋 — how can I help you today?"}
        ]
        st.error(f"Could not fetch chat history: {e}")


# --- CUSTOM CSS ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}

        .main {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background-color: var(--background-color);
            border: 1px solid rgba(100, 100, 100, 0.2);
            border-radius: 1rem;
            box-shadow: 0 0 15px rgba(0,0,0,0.15);
            padding: 1rem;
            overflow-y: auto;
        }

        .chat-row {
            display: flex;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }

        .assistant-row {
            flex-direction: row;
        }

        .user-row {
            flex-direction: row-reverse;
        }

        .chat-bubble {
            padding: 0.6rem 0.9rem;
            border-radius: 1.2rem;
            max-width: 75%;
            line-height: 1.4;
            font-size: 0.9rem;
            word-wrap: break-word;
        }

        .assistant-bubble {
            background-color: rgba(100, 149, 237, 0.15);
            border: 1px solid rgba(100, 149, 237, 0.3);
            color: inherit;
            border-top-left-radius: 0.3rem;
            box-shadow: 0px 1px 4px rgba(0,0,0,0.1);
        }

        .user-bubble {
            background-color: rgba(0, 128, 0, 0.15);
            border: 1px solid rgba(0, 128, 0, 0.3);
            color: inherit;
            border-top-right-radius: 0.3rem;
            margin-left: auto;
            text-align: right;
            box-shadow: 0px 1px 4px rgba(0,0,0,0.1);
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            margin: 0 0.5rem;
            object-fit: cover;
            box-shadow: 0 0 3px rgba(0,0,0,0.2);
        }

        .cursor {
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0% {opacity: 1;}
            50% {opacity: 0;}
            100% {opacity: 1;}
        }

        .stChatInput {
            position: fixed;
            bottom: 20px;
            width: 90%;
        }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I’m Richard 👋 — how can I help you today?"}
    ]

# --- ICONS ---
RICHARD_ICON = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_ICON = "https://cdn-icons-png.flaticon.com/512/1077/1077012.png"

# --- CHAT UI ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(
                f"""
                <div class='chat-row assistant-row'>
                    <img src='{RICHARD_ICON}' class='avatar'>
                    <div class='chat-bubble assistant-bubble'>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div class='chat-row user-row'>
                    <img src='{USER_ICON}' class='avatar'>
                    <div class='chat-bubble user-bubble'>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

# --- INPUT ---
if prompt := st.chat_input("Write a message..."):
    # --- User message ---
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
        <div class='chat-row user-row'>
            <img src='{USER_ICON}' class='avatar'>
            <div class='chat-bubble user-bubble'>{prompt}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- Send to backend ---
    try:
        res = requests.post(f"{API_URL}/ask", json={"message": prompt})
        if res.status_code == 200:
            data = res.json()
            reply = data.get("reply", "⚠️ No response from bot.")
        else:
            reply = f"⚠️ Server error: {res.status_code}"
    except Exception as e:
        reply = f"⚠️ Connection error: {e}"

    # --- Assistant reply ---
    placeholder = st.empty()
    full = ""
    for word in reply.split():
        full += word + " "
        placeholder.markdown(
            f"""
            <div class='chat-row assistant-row'>
                <img src='{RICHARD_ICON}' class='avatar'>
                <div class='chat-bubble assistant-bubble'>{full}<span class='cursor'>▌</span></div>
            </div>
            """,
            unsafe_allow_html=True)
        time.sleep(0.05)

    placeholder.markdown(
        f"""
        <div class='chat-row assistant-row'>
            <img src='{RICHARD_ICON}' class='avatar'>
            <div class='chat-bubble assistant-bubble'>{full}</div>
        </div>
        """,
        unsafe_allow_html=True)

    # --- Save reply locally ---
    st.session_state.messages.append({"role": "assistant", "content": reply})

