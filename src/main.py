import os
from flask import Flask
from flask_cors import CORS
from src.db import init_db
from src.router.chat_router import chat_bp
from src.util.clear_chat_db import init_scheduler
from src.middlewares import limiter

app = Flask(__name__)

# Allow CORS from any origin (you can restrict this to your Streamlit app URL later)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize rate limiter
limiter.init_app(app)

init_db()
init_scheduler(app)

@app.route('/')
def home():
    return {"status": "Server is running!", "message": "Chatbot backend API v1.0"}

app.register_blueprint(chat_bp)

if __name__ == '__main__':
    # Use environment variables for host and port (Render sets PORT automatically)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)