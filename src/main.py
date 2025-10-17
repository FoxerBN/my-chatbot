from flask import Flask
from flask_cors import CORS
from src.db import init_db
from src.router.chat_router import chat_bp
from src.util.clear_chat_db import init_scheduler

app = Flask(__name__)
CORS(app)
init_db()
init_scheduler(app)

@app.route('/')
def home():
    return "Server is running!"

app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#  flask --app src.main run --debug