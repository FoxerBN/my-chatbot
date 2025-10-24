from sqlalchemy import Column, Integer, String, DateTime, Text
from src.db import Base
import datetime
import json

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(100), index=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    expires_at = Column(DateTime, nullable=True)
    messages_json = Column(Text, default="[]")

    def add_message(self, role, content):
        messages = json.loads(self.messages_json)
        messages.append({"role": role, "content": content})
        self.messages_json = json.dumps(messages)
        self.updated_at = utcnow()

    def get_messages(self):
        return json.loads(self.messages_json)