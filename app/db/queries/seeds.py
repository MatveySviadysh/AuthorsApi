from sqlalchemy import insert
from db.database import sync_engine
from db.session import session_factory, acync_session_factory
from db.models.author import AuthorsORM, metadata
from db.base import Base
def create_tables():
    sync_engine.echo = True
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.echo = True

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
            AuthorsORM(
                first_name="Лев",
                last_name="Толстой",
                patronymic="Николаевич", 
                birth_date="1828-09-09",
                death_date="1910-11-20",
                bio="Один из наиболее известных русских писателей и мыслителей",
                photo="tolstoy.jpg"
            )
        ]
        session.add_all(authors)
        session.commit()
