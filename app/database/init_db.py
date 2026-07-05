from app.database.base import Base
from app.database.session import engine

# Important: import models so SQLAlchemy knows about them
from app.models.conversation import Conversation, ConversationMessage  # noqa: F401


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)