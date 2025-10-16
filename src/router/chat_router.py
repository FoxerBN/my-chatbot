from flask import Blueprint, request, jsonify
from src.service.openai_chatbot import ask_gpt

# Blueprint s prefixom /ai
chat_bp = Blueprint("chat", __name__, url_prefix="/ai")

@chat_bp.route("/ask", methods=["POST"])
def ask_route():
    """Jednoduchá API route pre volanie GPT-4"""
    data = request.get_json()
    user_msg = data.get("message", "")

    if not user_msg:
        return jsonify({"error": "Missing 'message' field"}), 400

    answer = ask_gpt(user_msg)
    return jsonify({"reply": answer})
