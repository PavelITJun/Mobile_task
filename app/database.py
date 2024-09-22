from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """
    FastAPI dependency that yields a database session.

    The session is automatically committed or rolled back at the end of the
    request, depending on whether an exception was thrown.
    """
    async with async_session_maker() as session:
        yield session
