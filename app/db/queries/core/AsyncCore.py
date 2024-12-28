from sqlalchemy import insert, select, update
from db.models.author_core_model import metadata_obj, authors_table, quotes_table
from db.database import async_engine

class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)
    
    @staticmethod
    async def insert_date():
        async with async_engine.connect() as conn:
            stmt = insert(authors_table).values(
                first_name="Александр",
                last_name="Пушкин", 
                patronymic="Сергеевич",
                birth_date="1799-06-06",
                death_date="1837-02-10",
                bio="Великий русский поэт, драматург и прозаик",
                photo="pushkin.jpg"
            )
            await conn.execute(stmt)
            await conn.commit()

    
    @staticmethod
    async def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        async with async_engine.connect() as conn:
            stmt = (
                update(authors_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def select_authors_and_quotes():
        async with async_engine.connect() as conn:
            query = select(authors_table, quotes_table.c.text).join(
                quotes_table, 
                authors_table.c.id == quotes_table.c.author_id
            )
            result = await conn.execute(query)
            print(result.all())


    @staticmethod
    async def select_workers_with_lazy_relationship():
        async with async_engine.connect() as conn:
            query = select(authors_table)
            result = await conn.execute(query)
            print(result.all())

    
    @staticmethod
    async def select_workers_with_joined_relationship():
        async with async_engine.connect() as conn:
            query = select(authors_table).join(quotes_table)
            result = await conn.execute(query)
            print(result.all())


    @staticmethod
    async def select_workers_with_selectin_relationship():
        async with async_engine.connect() as conn:
            query = select(authors_table).join(quotes_table)
            result = await conn.execute(query)
            print(result.all())