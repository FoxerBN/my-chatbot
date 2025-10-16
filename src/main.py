from flask import Flask
from src.db import init_db
from src.router.chat_router import chat_bp
app = Flask(__name__)
init_db()


@app.route('/')
def home():
    return "Server is running!"

app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#  flask --app src.main run --debug