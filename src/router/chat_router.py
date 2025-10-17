from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from src.db import SessionLocal
from src.service.openai_chatbot import ask_gpt
from src.service.save_chat import save_chat_message
from src.service.get_chat import get_chat_by_ip
chat_bp = Blueprint("chat", __name__, url_prefix="/ai")

@chat_bp.route("/ask", methods=["POST"])
def ask_route():
    data = request.get_json()
    user_msg = data.get("message", "")
    ip_address = request.remote_addr

    if not user_msg:
        return jsonify({"error": "Missing 'message' field"}), 400

    db: Session = SessionLocal()
    try:
        # 1️⃣ Načítaj posledných 10 správ ako kontext
        chat_history = get_chat_by_ip(db, ip_address)

        # chat_history by malo vyzerať napr. ako zoznam dictov:
        # [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
        # ak nie, tu to transformuj
        if chat_history and isinstance(chat_history, list):
            context_messages = chat_history[-10:]  # posledných 10
        else:
            context_messages = []

        # 2️⃣ Pošli prompt s kontextom
        answer = ask_gpt(user_msg, context_messages=context_messages)

        # 3️⃣ Ulož iba túto výmenu
        save_chat_message(db, ip_address, user_msg, answer)

        # 4️⃣ Odpoveď pre klienta
        return jsonify({"reply": answer})

    except Exception as e:
        print("Error processing chat:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()




@chat_bp.route("/fetch_chat", methods=["GET"])
def fetch_chat_route():
    ip_address = request.remote_addr or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if not ip_address:
        return jsonify({"error": "Unable to determine client IP"}), 400

    db: Session = None
    try:
        db = SessionLocal()
        user_messages = get_chat_by_ip(db, ip_address)
        return jsonify({"messages": user_messages})
    except Exception as e:
        print("Error fetching chat:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()
