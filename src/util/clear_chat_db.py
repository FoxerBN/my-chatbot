from flask_apscheduler import APScheduler

class Config:
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()


def clear_expired_chats():
    """Function to clear expired chats from the database."""
    from src.db import SessionLocal
    from src.model.chat_model import Chat
    import datetime

    db = SessionLocal()
    try:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        expired_chats = db.query(Chat).filter(Chat.expires_at != None, Chat.expires_at < now_utc).all()
        for chat in expired_chats:
            db.delete(chat)
        db.commit()
        print(f"Cleared {len(expired_chats)} expired chats.")
    except Exception as e:
        print(f"Error clearing expired chats: {e}")
    finally:
        db.close()


def init_scheduler(app):
    app.config.from_object(Config())

    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
        id='clear_expired_chats_job',
        func=clear_expired_chats,
        trigger='interval',
        minutes=1,
        replace_existing=True
    )

    print("Scheduler initialized and job started.")
