import datetime
import json
from sqlalchemy.orm import Session
from src.model.chat_model import Chat

EXPIRATION_HOURS = 1


def save_chat_message(db: Session, ip_address: str, user_text: str, bot_text: str):
    """
    Save or update chat messages in the database based on IP address.
    Uses timezone-aware UTC datetimes.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now_utc + datetime.timedelta(hours=EXPIRATION_HOURS)

    chat = db.query(Chat).filter(Chat.ip_address == ip_address).first()

    if not chat:
        chat = Chat(
            ip_address=ip_address,
            created_at=now_utc,
            updated_at=now_utc,
            expires_at=expires_at,
            messages_json=json.dumps([]),
        )
        db.add(chat)
    else:
        chat.updated_at = now_utc

    chat.add_message("user", user_text)
    chat.add_message("assistant", bot_text)

    chat.expires_at = expires_at

    db.commit()
    db.refresh(chat)
    return chat
