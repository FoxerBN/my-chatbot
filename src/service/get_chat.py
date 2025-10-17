from sqlalchemy.orm import Session
from src.model.chat_model import Chat


def get_chat_by_ip(db: Session, ip: str, limit: int = 10):
    chat = db.query(Chat).filter(Chat.ip_address == ip).first()
    if not chat:
        return []

    try:
        messages = chat.get_messages()
        return messages[-limit:]
    except Exception as e:
        print("Error decoding messages for chat:", e)
        return []
