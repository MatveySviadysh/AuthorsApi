from datetime import datetime
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    CheckConstraint,
    text
)

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

quotes_table = Table(
    "quotes",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True, nullable=False),
    Column("text", String(200), nullable=False),
    Column("created_at", Date, server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", Date, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow),
    Column("year", Integer, CheckConstraint("year >= 0 AND year <= extract(year from CURRENT_DATE)"), nullable=True),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
)