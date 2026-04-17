from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from config.db_engine import engine
from schemas.chat_schema import ChatHistory
from datetime import datetime
from typing import Generator, Any

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Manages the database session lifecycle.
    Ensures the connection is always closed and returned to the pool,
    even if exceptions occur during execution.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_or_update_chat(
    chat_id: int | None,
    messages: list[dict[str, Any]],
    user_id: int = 1,
    title: str | None = None
) -> int:
    """
    Persists a new chat session or updates an existing one in the database.
    """
    data_atual = datetime.now()
    # Generate an automated title if none is provided
    title = title if title else f"Conversa {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

    with get_db_session() as session:
        if chat_id is None:
            new_chat = ChatHistory(
                user_id=user_id,
                title=title,
                chat_history=messages,
                timestamp=data_atual
            )
            session.add(new_chat)
            session.commit()
            session.refresh(new_chat)
            return new_chat.id
        else:
            chat = session.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
            if chat:
                chat.chat_history = messages
                session.commit()
                return chat.id
            else:
                new_chat = ChatHistory(
                    user_id=user_id,
                    title=title,
                    chat_history=messages,
                    timestamp=data_atual
                )
                session.add(new_chat)
                session.commit()
                session.refresh(new_chat)
                return new_chat.id

def get_user_chats(user_id: int = 1) -> list[dict[str, Any]]:
    """
    Retrieves previous chat sessions for a specific user, ordered by most recent.
    """
    with get_db_session() as session:
        chats = (
            session
            .query(ChatHistory.id, ChatHistory.title)
            .filter(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.id.desc()).all()
        )
        return [{"id": chat.id, "title": chat.title} for chat in chats]

def get_chat_messages(chat_id: int) -> list[dict[str, Any]]:
    """
    Loads the message history for a specific chat ID.
    """
    with get_db_session() as session:
        chat = session.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
        if chat:
            return chat.chat_history
        return []