from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from db.base import Base
from db.database import async_engine
from db.models.author_orm_model import AuthorsORM, QuotesORM
from db.session import async_session_factory

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


    @staticmethod
    async def insert_workers():
        async with async_session_factory() as session:
            worker_jack = AuthorsORM(username="Jack")
            worker_michael = AuthorsORM(username="Michael")
            session.add_all([worker_jack, worker_michael])
            await session.flush()
            await session.commit()

    
    @staticmethod
    async def select_authors_and_quotes():
        async with async_session_factory() as session:
            query = select(AuthorsORM, QuotesORM.text).join(
                QuotesORM,
                AuthorsORM.id == QuotesORM.author_id
            )
            result = await session.execute(query)
            print(result.all())

    
    @staticmethod
    async def select_workers_with_lazy_relationship():
        async with async_session_factory() as session:
            query = select(AuthorsORM)
            res = await session.execute(query)
            authors = res.scalars().all()
            print(authors)


    @staticmethod
    async def select_workers_with_joined_relationship():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(joinedload(AuthorsORM.quotes))
            )
            res = await session.execute(query)
            authors = res.unique().scalars().all()
            print(authors)
    

    @staticmethod
    async def select_workers_with_selectin_relationship():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(selectinload(AuthorsORM.quotes))
            )
            res = await session.execute(query)
            authors = res.unique().scalars().all()
            print(authors)