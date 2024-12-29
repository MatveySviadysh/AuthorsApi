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
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    quotes: Mapped[list["QuotesORM"]] = relationship(
        "QuotesORM",
        back_populates="author",
        primaryjoin="and_(AuthorsORM.id == QuotesORM.author_id, QuotesORM.text == 'parttime')",
        order_by="QuotesORM.id.desc()"
    )

    @property
    def full_name(self) -> str:
        parts = []
        if self.last_name:
            parts.append(self.last_name)
        if self.first_name:
            parts.append(self.first_name)
        if self.patronymic:
            parts.append(self.patronymic)
        return " ".join(parts)
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "photo": self.photo,
            "bio": self.bio,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "death_date": self.death_date.isoformat() if self.death_date else None,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class QuotesORM(Base):
    __tablename__ = "quotes"

    id: Mapped[intpk]
    text: Mapped[str_200_nullable_false]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    year: Mapped[year]
    
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    author: Mapped["AuthorsORM"] = relationship("AuthorsORM", back_populates="quotes")
