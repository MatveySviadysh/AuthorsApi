from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from .database import sync_engine, async_engine

session_factory = sessionmaker(bind=sync_engine)
async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
