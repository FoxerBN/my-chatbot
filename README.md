# 🤖 My Chatbot

A lightweight, intelligent chatbot built with Flask and powered by OpenAI, featuring automated conversation history management and AI guardrails for safe interactions.

## 📝 Description

This is a Flask-based chatbot API that serves as Richard Tekula's portfolio assistant. It stores conversation history in SQLite and automatically cleans up messages older than 1 hour to maintain efficiency. The bot is designed to answer questions about Richard's skills, projects, experience, and tech stack.

## ✨ Features

- 💬 **OpenAI Integration** - Powered by GPT for intelligent conversations
- 🛡️ **AI Guardrails** - Built-in content filtering and safety checks
- 💾 **Persistent Storage** - SQLite database for conversation history
- 🧹 **Auto-cleanup** - Scheduled task removes messages older than 1 hour
- 🌐 **CORS Enabled** - Ready for frontend integration
- 🚀 **Production Ready** - Configured for deployment with Gunicorn

## 📁 Project Structure

```
my-chatbot/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Flask app initialization & routes
│   ├── config.py                  # Environment variables & settings
│   ├── db.py                      # Database setup & session management
│   ├── prompt.py                  # System prompt for chatbot personality
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   └── chat_model.py          # SQLAlchemy chat message model
│   │
│   ├── router/
│   │   ├── __init__.py
│   │   └── chat_router.py         # Chat API endpoints
│   │
│   ├── service/
│   │   ├── __init__.py
│   │   ├── openai_chatbot.py     # OpenAI API integration
│   │   ├── guardrails_ai.py      # Content moderation & safety
│   │   ├── save_chat.py          # Save messages to database
│   │   └── get_chat.py           # Retrieve chat history
│   │
│   └── util/
│       ├── __init__.py
│       ├── clear_chat_db.py      # Scheduled cleanup task
│       └── helpers.py            # Utility functions
│
├── requirements.txt               # Python dependencies
├── Procfile                       # Deployment configuration
└── chatbot.db                     # SQLite database (auto-generated)
```

## 🔧 How It Works

### 1️⃣ **Request Flow**
```
User sends message → Flask API → Guardrails check → OpenAI API → Response → Save to DB
```

### 2️⃣ **Components Breakdown**

**🔹 Main Application (`main.py`)**
- Initializes Flask app with CORS
- Registers chat routes
- Starts background scheduler for cleanup

**🔹 Configuration (`config.py`)**
- Loads environment variables (OpenAI API key, DB URL, etc.)
- Sets data expiration time (default: 1 hour)

**🔹 Database Layer (`db.py` + `chat_model.py`)**
- SQLAlchemy ORM setup
- Chat message model with timestamps
- Session management

**🔹 Chat Router (`chat_router.py`)**
- POST `/chat` - Send message and get AI response
- GET `/chat/history` - Retrieve conversation history

**🔹 Services**
- **openai_chatbot.py** - Sends prompts to OpenAI API
- **guardrails_ai.py** - Validates input/output for safety
- **save_chat.py** - Persists messages to database
- **get_chat.py** - Fetches chat history

**🔹 Utilities**
- **clear_chat_db.py** - APScheduler job that runs every hour to delete old messages

### 3️⃣ **Data Expiration**
The scheduler automatically removes messages older than 1 hour:
```python
# Runs every hour
Job → Check timestamps → Delete old records → Keep DB clean
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Step 1: Clone the repository
```bash
git clone https://github.com/FoxerBN/my-chatbot.git
cd my-chatbot
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set up environment variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DB_URL=sqlite:///chatbot.db
DEBUG=False
DATA_EXPIRATION_HOURS=1
```

### Step 4: Run the application
```bash
# Development
python -m src.main

# Production (with Gunicorn)
gunicorn --bind 0.0.0.0:5000 src.main:app
```

## 📡 API Endpoints

### Send Message
```http
POST /chat
Content-Type: application/json

{
  "message": "Tell me about your projects"
}
```

**Response:**
```json
{
  "response": "AI-generated response here"
}
```

### Get Chat History
```http
GET /chat/history
```

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello",
      "timestamp": "2025-10-25T07:30:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Hi! How can I help?",
      "timestamp": "2025-10-25T07:30:05"
    }
  ]
}
```

## 📦 Dependencies

- **flask** - Web framework
- **flask-cors** - CORS handling
- **openai** - OpenAI API client
- **sqlalchemy** - Database ORM
- **python-dotenv** - Environment variables
- **Flask-APScheduler** - Background job scheduling
- **gunicorn** - WSGI HTTP server

## 🌐 Deployment

The app is configured for deployment on platforms like Render, Heroku, or Railway using the included `Procfile`:

```
web: gunicorn --bind 0.0.0.0:$PORT src.main:app
```

## 🔒 Security Features

- Input validation with AI guardrails
- Content moderation for safe responses
- Environment-based configuration
- No sensitive data in codebase

## 👨‍💻 Author

**Richard Tekula (FoxerBN)**
- Portfolio: [foxerbn.github.io/sk](https://foxerbn.github.io/sk)
- GitHub: [@FoxerBN](https://github.com/FoxerBN)

## 📄 License

This project is open source and available under the MIT License.

---

Made with ❤️ by Richard Tekula
```
