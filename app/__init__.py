from .config.db_engine import engine
from .schemas.chat_schema import Base

# Ensure all database tables exist
Base.metadata.create_all(engine)
