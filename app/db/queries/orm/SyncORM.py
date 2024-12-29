from db.base import Base
from db.database import sync_engine
from db.models.author_orm_model import AuthorsORM, QuotesORM
from db.session import session_factory
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, contains_eager


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        #Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True
        

    @staticmethod
    def insert_data():
        with session_factory() as session:
            session.execute(AuthorsORM.__table__.delete())
            authors = [
                AuthorsORM(
                    first_name="Александр",
                    last_name="Пушкин", 
                    patronymic="Сергеевич",
                    birth_date="1799-06-06",
                    death_date="1837-02-10",
                    bio="Великий русский поэт, драматург и прозаик",
                    photo="pushkin.jpg"
                ),
            ]
            session.add_all(authors)
            session.flush() # сохраняет объект в базу данных
            session.commit()


    @staticmethod
    def select_authors():
        with session_factory() as session:
            query = select(AuthorsORM)
            res = session.execute(query)
            authors = res.scalars().all()
            print(f"Авторы: {authors}")

    
    @staticmethod
    def update_author(author_id: int, new_first_name: str, new_last_name: str, new_patronymic: str, new_birth_date: str, new_death_date: str, new_bio: str, new_photo: str):
        with session_factory() as session:
            author = session.get(AuthorsORM, author_id)
            if author:
                author.first_name = new_first_name
                author.last_name = new_last_name
                author.patronymic = new_patronymic
                author.birth_date = new_birth_date
                author.death_date = new_death_date
                author.bio = new_bio
                author.photo = new_photo
                session.commit()
                print(f"Автор обновлен: {author}")
            else:
                print(f"Автор с id={author_id} не найден")


    @staticmethod
    def select_authors_and_quotes():
        with session_factory() as session:
            query = select(
                AuthorsORM.id,
                AuthorsORM.first_name,
                QuotesORM.text,
                QuotesORM.year
            ).join(
                QuotesORM,
                AuthorsORM.id == QuotesORM.author_id
            )
            result = session.execute(query)
            print(result.all())


    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = select(AuthorsORM)
            res = session.execute(query) # выполняет запрос и возвращает результат
            authors = res.scalars().all()
            
            if len(authors) >= 2:
                author1_quotes = authors[0].quotes
                author2_quotes = authors[1].quotes
                print(author1_quotes + author2_quotes)
            else:
                print("Недостаточно авторов в базе данных")


    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(joinedload(AuthorsORM.quotes))# загружает сразу все цитаты решение проблемы n + 1
            ) 
            res = session.execute(query)
            authors = res.unique().scalars().all()

            if len(authors) >= 2:
                author1_quotes = authors[0].quotes
                author2_quotes = authors[1].quotes
                print(author1_quotes + author2_quotes)
            else:
                print("Недостаточно авторов в базе данных")
    
    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(selectinload(AuthorsORM.quotes)) # сначала загружает авторов, потом цитаты
            )
            res = session.execute(query)
            authors = res.unique().scalars().all()

            if len(authors) >= 2:
                author1_quotes = authors[0].quotes
                author2_quotes = authors[1].quotes
                print(author1_quotes + author2_quotes)
            else:
                print("Недостаточно авторов в базе данных")


    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(AuthorsORM)
                .options(selectinload(AuthorsORM.quotes_parttime))
            )
            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(AuthorsORM)
                .join(AuthorsORM.resumes)
                .options(contains_eager(AuthorsORM.resumes))
                .filter(QuotesORM.workload == 'parttime')
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_relationship_contains_eager_with_limit():
        with session_factory() as session:
            subq = (
                select(QuotesORM.id.label("parttime_resume_id"))
                .filter(QuotesORM.worker_id == AuthorsORM.id)
                .order_by(AuthorsORM.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(AuthorsORM)
            )

            query = (
                select(AuthorsORM)
                .join(QuotesORM, QuotesORM.id.in_(subq))
                .options(contains_eager(AuthorsORM.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)
