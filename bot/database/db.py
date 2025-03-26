from sqlalchemy.ext.asyncio import create_async_engine
from bot.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
