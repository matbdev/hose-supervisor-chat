from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON, DateTime

Base = declarative_base()

class ChatHistory(Base):
    """
    Schema for persisting chat conversations including metadata and raw history.
    """
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    chat_history = Column(JSON)
    timestamp = Column(DateTime)