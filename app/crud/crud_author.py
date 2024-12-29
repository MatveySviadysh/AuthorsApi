from fastcrud import FastCRUD
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import select

from db.models.author_orm_model import AuthorsORM
from schemas.author import Author, AuthorUpdate, AuthorCreateInternal, AuthorUpdateInternal, AuthorDelete


class CRUDAuthor:
    def __init__(self, model: AuthorsORM):
        self.model = model

    async def create(self, db: Session, *, obj_in: AuthorCreateInternal) -> Author:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, id: int) -> Optional[Author]:
        return db.get(self.model, id)

    async def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Author]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = db.execute(stmt)
        return result.scalars().all()

    async def update(self, db: Session, *, db_obj: AuthorsORM, obj_in: AuthorUpdate) -> Author:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, *, id: int) -> Optional[AuthorDelete]:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
            return AuthorDelete(id=id, is_deleted=True)
        return None


crud_authors = CRUDAuthor(AuthorsORM)