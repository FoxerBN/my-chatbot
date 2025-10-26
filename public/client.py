import streamlit as st
import time
import requests
import markdown
import html
import os

# Use Streamlit secrets or environment variable for API URL
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:5000/ai"))
except:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/ai")

# Page config
st.set_page_config(
    page_title="Richard Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Allow iframe embedding
st.markdown(
    "<meta http-equiv='Content-Security-Policy' content='frame-ancestors *;'>",
    unsafe_allow_html=True
)

# Custom CSS
st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        .stDeployButton {display: none;}

        /* Reset margins and padding for iframe */
        html, body {
            margin: 0;
            padding: 0;
            background-color: #0E1117;
            height: 100vh;
            overflow: hidden;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #0E1117;
            padding: 0;
            margin: 0;
        }

        .block-container {
            padding: 1rem 1rem 0rem 1rem;
            max-width: 800px;
            margin: 0 auto;
            width: 95%;
        }

        .main {
            padding: 0;
            margin: 0;
            height: 100vh;
            overflow-y: auto;
            padding-bottom: 100px;
            scroll-behavior: smooth;
        }

        /* Chat bubbles */
        .chat-row {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }

        .assistant-row {
            flex-direction: row;
        }

        .user-row {
            flex-direction: row-reverse;
        }

        .chat-bubble {
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            max-width: 80%;
            line-height: 1.5;
            font-size: 0.95rem;
            word-wrap: break-word;
        }

        .assistant-bubble {
            background-color: rgba(100, 149, 237, 0.15);
            border: 1px solid rgba(100, 149, 237, 0.3);
            color: inherit;
            border-top-left-radius: 0.3rem;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
        }

        .user-bubble {
            background-color: rgba(0, 128, 0, 0.15);
            border: 1px solid rgba(0, 128, 0, 0.3);
            color: inherit;
            border-top-right-radius: 0.3rem;
            margin-left: auto;
            text-align: right;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            margin: 0 0.6rem;
            object-fit: cover;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .cursor {
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0% {opacity: 1;}
            50% {opacity: 0;}
            100% {opacity: 1;}
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        /* Chat input - only position and width */
        .stChatInput {
            position: fixed;
            bottom: 10px;
            left: 50%;
            width: 90%;
            transform: translateX(-50%);
            max-width: 800px;
        }
        
        .stChatInput > div {
            width: 100%;    
        }
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0E1117">
    <script>
        // Auto-scroll to bottom
        function scrollToBottom() {
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            }, 100);
        }
        window.addEventListener('load', scrollToBottom);
        const observer = new MutationObserver(scrollToBottom);
        setTimeout(() => {
            const target = document.querySelector('.main');
            if (target) {
                observer.observe(target, { childList: true, subtree: true });
            }
        }, 500);
    </script>
""", unsafe_allow_html=True)

# Avatar URLs
RICHARD_ICON = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_ICON = "https://cdn-icons-png.flaticon.com/512/1077/1077012.png"

# Initialize chat history
if "messages" not in st.session_state:
    try:
        res = requests.get(f"{API_URL}/fetch_chat", timeout=5)
        if res.status_code == 200:
            data = res.json()
            st.session_state.messages = data.get("messages", [])
            if not st.session_state.messages:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem dnes pomôcť ?"}
                ]
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem dnes pomôcť ?"}
            ]
    except Exception as e:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ahoj, ja som Richard 👋 — ako ti môžem dnes pomôcť ?"}
        ]

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# Display chat messages with custom bubbles
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

    # Show thinking indicator if waiting
    if st.session_state.waiting_for_response:
        st.markdown(f"""
            <div class='chat-row assistant-row'>
                <img src='{RICHARD_ICON}' class='avatar'>
                <div class='chat-bubble assistant-bubble'>Thinking<span class='cursor'>▌</span></div>
            </div>
        """, unsafe_allow_html=True)

# Native Streamlit input
if prompt := st.chat_input("Write a message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.waiting_for_response = True
    st.rerun()

# Process waiting response
if st.session_state.waiting_for_response:
    last_user_message = [msg for msg in st.session_state.messages if msg["role"] == "user"][-1]["content"]

    try:
        res = requests.post(f"{API_URL}/ask", json={"message": last_user_message}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            reply = data.get("reply", "⚠️ No response from bot.")
        else:
            reply = f"⚠️ Server error: {res.status_code}"
    except Exception as e:
        reply = f"⚠️ Connection error: {e}"

    # Clear waiting state
    st.session_state.waiting_for_response = False

    # Convert markdown to HTML
    reply_html = markdown.markdown(
        reply,
        extensions=['extra', 'nl2br'],
        output_format='html'
    ).replace('\n', '<br>')

    # Typing animation
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

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
