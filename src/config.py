import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set in environment variables.")

# --- Database ---
DB_URL = os.getenv("DB_URL", "sqlite:///chatbot.db")

# --- Application settings ---
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATA_EXPIRATION_HOURS = int(os.getenv("DATA_EXPIRATION_HOURS", 1))

# --- Routes ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../chatbot.db")

print(f"✅ Config loaded: DB_URL={DB_URL}, DEBUG={DEBUG}")
