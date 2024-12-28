from sqlalchemy import insert, text, select, update, delete
from db.database import sync_engine, async_engine
from db.models.author import authors_table, metadata_obj
from db.base import Base


class SyncCore:
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)
        sync_engine.echo = True

    def insert_data():
        with sync_engine.connect() as conn:
            stmt = insert(authors_table).values(
                first_name="Александр",
                last_name="Пушкин", 
                patronymic="Сергеевич",
                birth_date="1799-06-06",
                death_date="1837-02-10",
                bio="Великий русский поэт, драматург и прозаик",
                photo="pushkin.jpg"
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_authors():
        with sync_engine.connect() as conn:
            query = select(authors_table)
            result = conn.execute(query)
            authors = result.mappings().all()
            for author in authors:
                print(
                    f"ID: {author.id}, "
                    f"Имя: {author.first_name}, "
                    f"Отчество: {author.patronymic}, "
                    f"Фамилия: {author.last_name}, "
                    f"Дата рождения: {author.birth_date}"
                )


    @staticmethod
    def update_author(author_id: int,new_first_name: str, new_last_name: str, new_patronymic: str, new_birth_date: str, new_death_date: str, new_bio: str, new_photo: str):
        with sync_engine.connect() as conn:
            stmt = (
                update(authors_table)
                .values(
                    first_name=new_first_name,
                    last_name=new_last_name,
                    patronymic=new_patronymic,
                    birth_date=new_birth_date,
                    death_date=new_death_date,
                    bio=new_bio,
                    photo=new_photo
                )
                # .where(workers_table.c.id==worker_id)
                .filter(authors_table.c.id == author_id)
            )
            conn.execute(stmt)
            conn.commit()

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