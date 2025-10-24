import streamlit as st
import time
import random
import requests
import markdown
import html
import os

# Use Streamlit secrets or environment variable for API URL (fallback to localhost)
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:5000/ai"))
except:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/ai")

st.set_page_config(
    page_title="Richard Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


if "messages" not in st.session_state:
    try:
        res = requests.get(f"{API_URL}/fetch_chat")
        if res.status_code == 200:
            data = res.json()
            st.session_state.messages = data.get("messages", [])
            if not st.session_state.messages:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem den pomôcť ?"}
                ]
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem den pomôcť ?"}
            ]
    except Exception as e:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem den pomôcť ?"}
        ]
        st.error(f"Could not fetch chat history: {e}")


# --- VIEWPORT & CUSTOM CSS ---
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        /* Hide Streamlit branding */
        #MainMenu, footer, header {visibility: hidden !important; display: none !important;}
        .stDeployButton {display: none !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        iframe {display: none !important;}

        /* Main container */
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
            padding-bottom: 80px;
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

        /* Chat input positioning */
        .stChatInput {
            position: fixed !important;
            bottom: 20px !important;
            width: 90% !important;
            z-index: 999 !important;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .main {
                position: fixed;
                bottom: 0;
                right: 0;
                left: 0;
                top: 0;
                width: 100%;
                height: 100vh;
                border-radius: 0;
                padding-bottom: 100px;
            }

            .stChatInput {
                bottom: 10px !important;
                left: 5% !important;
                width: 90% !important;
                position: fixed !important;
                z-index: 9999 !important;
            }

            [data-testid="stHeader"] {
                display: none !important;
                height: 0 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Richard 👋 — how can I help you today?"}
    ]

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# --- ICONS ---
RICHARD_ICON = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_ICON = "https://cdn-icons-png.flaticon.com/512/1077/1077012.png"

# --- CHAT UI ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            content_html = markdown.markdown(
                msg['content'],
                extensions=['extra', 'nl2br'],
                output_format='html'
            ).replace('\n', '<br>')
            st.markdown(
                f"""
                <div class='chat-row assistant-row'>
                    <img src='{RICHARD_ICON}' class='avatar'>
                    <div class='chat-bubble assistant-bubble'>{content_html}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            content_escaped = html.escape(msg['content']).replace('\n', '<br>')
            st.markdown(
                f"""
                <div class='chat-row user-row'>
                    <img src='{USER_ICON}' class='avatar'>
                    <div class='chat-bubble user-bubble'>{content_escaped}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Show thinking indicator if waiting ---
    if st.session_state.waiting_for_response:
        st.markdown(f"""
            <div class='chat-row assistant-row'>
                <img src='{RICHARD_ICON}' class='avatar'>
                <div class='chat-bubble assistant-bubble'>Thinking<span class='cursor'>▌</span></div>
            </div>
        """, unsafe_allow_html=True)

# --- INPUT ---
if prompt := st.chat_input("Write a message..."):
    # --- User message ---
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.waiting_for_response = True
    st.rerun()

# --- Process waiting response ---
if st.session_state.waiting_for_response:
    # --- Send to backend ---
    last_user_message = [msg for msg in st.session_state.messages if msg["role"] == "user"][-1]["content"]

    try:
        res = requests.post(f"{API_URL}/ask", json={"message": last_user_message})
        if res.status_code == 200:
            data = res.json()
            reply = data.get("reply", "⚠️ No response from bot.")
        else:
            reply = f"⚠️ Server error: {res.status_code}"
    except Exception as e:
        reply = f"⚠️ Connection error: {e}"

    # --- Clear waiting state ---
    st.session_state.waiting_for_response = False

    # --- Convert markdown to HTML ---
    reply_html = markdown.markdown(
        reply,
        extensions=['extra', 'nl2br'],
        output_format='html'
    ).replace('\n', '<br>')

    # --- Assistant reply with typing animation ---
    placeholder = st.empty()
    full = ""
    for word in reply.split():
        full += word + " "
        full_html = markdown.markdown(
            full,
            extensions=['extra', 'nl2br'],
            output_format='html'
        ).replace('\n', '<br>')
        placeholder.markdown(
            f"""
            <div class='chat-row assistant-row'>
                <img src='{RICHARD_ICON}' class='avatar'>
                <div class='chat-bubble assistant-bubble'>{full_html}<span class='cursor'>▌</span></div>
            </div>
            """,
            unsafe_allow_html=True)
        time.sleep(0.05)

    placeholder.markdown(
        f"""
        <div class='chat-row assistant-row'>
            <img src='{RICHARD_ICON}' class='avatar'>
            <div class='chat-bubble assistant-bubble'>{reply_html}</div>
        </div>
        """,
        unsafe_allow_html=True)

    # --- Save reply locally ---
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

