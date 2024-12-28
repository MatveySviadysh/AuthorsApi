from typing import List, Optional
from fastcrud import FastCRUD
from sqlalchemy.orm import Session

from db.models.author_orm_model import QuotesORM
from schemas.quotes import (
    Quote, 
    QuoteCreate, 
    QuoteCreateInternal, 
    QuoteUpdate, 
    QuoteUpdateInternal, 
    QuoteDelete
)

class CRUDQuote(FastCRUD[Quote, QuoteCreateInternal, QuoteUpdate, QuoteUpdateInternal, QuoteDelete]):
    async def get_by_author(self, db: Session, *, author_id: int) -> List[Quote]:
        return await db.query(self.model).filter(
            self.model.author_id == author_id
        ).all()

    async def get_by_year(self, db: Session, *, year: int) -> List[Quote]:
        return await db.query(self.model).filter(
            self.model.year == year
        ).all()

crud_quotes = CRUDQuote(QuotesORM)