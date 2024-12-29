from .models.author_core_model import metadata_obj
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import settings


sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL_PSYCOPG,
    echo=True,
    pool_size=5, 
    max_overflow=10
)

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL_ASYNC,
    echo=True,
    pool_size=5,
    max_overflow=10
)
