from datetime import datetime
from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    Date,
    text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from typing import Annotated


str_200_nullable_false = Annotated[str, mapped_column(String(200), nullable=False)]
str_200_nullable_true = Annotated[str, mapped_column(String(200), nullable=True)]


intpk = Annotated[int, mapped_column(primary_key=True,autoincrement=True,index=True,nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )]
year = Annotated[int, mapped_column(
        CheckConstraint("year >= 0 AND year <= extract(year from CURRENT_DATE)"),
        nullable=True
    )]

class AuthorsORM(Base):
    __tablename__ = "authors"

    id: Mapped[intpk]
    first_name: Mapped[str_200_nullable_true]
    last_name: Mapped[str_200_nullable_true]
    patronymic: Mapped[str | None] = mapped_column(String(100), nullable=True)
    photo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    death_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)

    quotes: Mapped[list["QuotesORM"]] = relationship("QuotesORM", back_populates="author")

    def __repr__(self):
        return f"Автор(id={self.id}, {self.first_name} {self.patronymic} {self.last_name})"

class QuotesORM(Base):
    __tablename__ = "quotes"

    id: Mapped[intpk]
    text: Mapped[str_200_nullable_false]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    year: Mapped[year]
    
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    author: Mapped["AuthorsORM"] = relationship("AuthorsORM", back_populates="quotes")


metadata_obj = MetaData()

authors_table = Table(
    "authors",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True, nullable=False),
    Column("first_name", String(200), nullable=True),
    Column("last_name", String(200), nullable=True), 
    Column("patronymic", String(100), nullable=True),
    Column("photo", String(255), nullable=True),
    Column("bio", Text, nullable=True),
    Column("birth_date", Date, nullable=False),
    Column("death_date", Date, nullable=True)
)