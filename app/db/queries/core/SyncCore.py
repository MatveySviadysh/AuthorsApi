from sqlalchemy import insert, text, select, update, delete, alias
from db.database import sync_engine
from db.models.author_core_model import authors_table, metadata_obj, quotes_table
from db.base import Base
from sqlalchemy.orm import lazyload, joinedload, selectinload

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
            query = select(authors_table) # SELECT * FROM authors
            res = conn.execute(query)
            authors = res.all()
            print(f"Авторы: {authors}")


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

    @staticmethod
    def  insert_quotes():
        with sync_engine.connect() as conn:
            authors = [
                {
                    "id": 1,
                    "first_name": "Антон",
                    "last_name": "Чехов",
                    "patronymic": "Павлович", 
                    "birth_date": "1860-01-29",
                    "death_date": "1904-07-15",
                    "bio": "Русский писатель, прозаик, драматург",
                    "photo": "chekhov.jpg"
                },
                {
                    "id": 2,
                    "first_name": "Михаил",
                    "last_name": "Лермонтов",
                    "patronymic": "Юрьевич",
                    "birth_date": "1814-10-15", 
                    "death_date": "1841-07-27",
                    "bio": "Русский поэт, прозаик, драматург",
                    "photo": "lermontov.jpg"
                },
                {
                    "id": 3,
                    "first_name": "Федор",
                    "last_name": "Достоевский",
                    "patronymic": "Михайлович",
                    "birth_date": "1821-11-11",
                    "death_date": "1881-02-09", 
                    "bio": "Русский писатель, мыслитель",
                    "photo": "dostoevsky.jpg"
                }
            ]
            stmt = insert(authors_table).values(authors)
            conn.execute(stmt)
            
            quotes = [
                {"text": "Краткость - сестра таланта", "year": 1889, "author_id": 1},
                {"text": "Если боитесь одиночества, то не женитесь", "year": 1893, "author_id": 1},
                {"text": "В человеке должно быть все прекрасно", "year": 1898, "author_id": 1},
                {"text": "Белеет парус одинокий", "year": 1832, "author_id": 2},
                {"text": "Выхожу один я на дорогу", "year": 1841, "author_id": 2},
                {"text": "Красота спасет мир", "year": 1868, "author_id": 3},
            ]
            stmt = insert(quotes_table).values(quotes)
            conn.execute(stmt)
            conn.commit()


    @staticmethod
    def select_authors_and_quotes():
        with sync_engine.connect() as conn:
            query = (
                select(
                    authors_table.c.id,
                    authors_table.c.first_name,
                    authors_table.c.last_name,
                    quotes_table.c.text.label('quote')
                )
                .join(
                    quotes_table,
                    authors_table.c.id == quotes_table.c.author_id
                )
                .order_by(authors_table.c.id)
            )
            result = conn.execute(query)
            print(result.all())


    @staticmethod
    def select_workers_with_lazy_relationship():
        with sync_engine.connect() as conn:
            query = select(authors_table).options(lazyload(authors_table.quotes))
            result = conn.execute(query)
            print(result.all())

    
    @staticmethod
    def select_workers_with_joined_relationship():
        with sync_engine.connect() as conn:
            query = select(authors_table).options(joinedload(authors_table.quotes))
            result = conn.execute(query)
            print(result.all())


    @staticmethod
    def select_workers_with_selectin_relationship():
        with sync_engine.connect() as conn:
            query = select(authors_table).options(selectinload(authors_table.quotes))
            result = conn.execute(query)
            print(result.all())

