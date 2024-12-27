from sqlalchemy import Column, Integer, String, Table, MetaData, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped,mapped_column
from db.base import Base



class AuthorsORM(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    patronymic = Column(String(100), nullable=True)
    photo = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=False)
    death_date = Column(Date, nullable=True)

metadata = MetaData()
