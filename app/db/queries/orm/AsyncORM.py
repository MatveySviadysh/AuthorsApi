from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, contains_eager
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
    async def get_authors_with_quotes():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM, QuotesORM.text)
                .join(QuotesORM, AuthorsORM.id == QuotesORM.author_id)
            )
            result = await session.execute(query)
            return result.all()

    @staticmethod
    async def select_workers_with_lazy_relationship():
        async with async_session_factory() as session:
            query = select(AuthorsORM)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_authors_with_quotes_joined():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(joinedload(AuthorsORM.quotes))
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    @staticmethod
    async def select_workers_with_selectin_relationship():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(selectinload(AuthorsORM.quotes))
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    @staticmethod
    async def select_workers_with_condition_relationship():
        async with async_session_factory() as session:
            query = (
                select(AuthorsORM)
                .join(AuthorsORM.quotes)
                .options(contains_eager(AuthorsORM.quotes))
                .filter(QuotesORM.workload == 'parttime')
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    @staticmethod
    async def select_workers_with_relationship_contains_eager_with_limit():
        async with async_session_factory() as session:
            subquery = (
                select(QuotesORM.id)
                .filter(QuotesORM.author_id == AuthorsORM.id)
                .order_by(QuotesORM.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(AuthorsORM)
            )
            query = (
                select(AuthorsORM)
                .join(QuotesORM, QuotesORM.id.in_(subquery))
                .options(contains_eager(AuthorsORM.quotes))
            )
            result = await session.execute(query)
            return result.unique().scalars().all()