from fastcrud import FastCRUD
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import select

from db.models.author_orm_model import QuotesORM
from schemas.quotes import Quote, QuoteCreateInternal, QuoteUpdate, QuoteUpdateInternal, QuoteDelete


class CRUDQuote:
    def __init__(self, model: QuotesORM):
        self.model = model

    async def create(self, db: Session, *, obj_in: QuoteCreateInternal) -> Quote:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, id: int) -> Optional[Quote]:
        return db.get(self.model, id)

    async def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Quote]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = db.execute(stmt)
        return result.scalars().all()

    async def update(self, db: Session, *, db_obj: QuotesORM, obj_in: QuoteUpdate) -> Quote:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, *, id: int) -> Optional[QuoteDelete]:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
            return QuoteDelete(id=id, is_deleted=True)
        return None


crud_quotes = CRUDQuote(QuotesORM)
