from typing import List, Optional
from fastcrud import FastCRUD
from sqlalchemy.orm import Session

from db.models.author_orm_model import AuthorsORM
from schemas.author import (
    Author, 
    AuthorCreate, 
    AuthorCreateInternal, 
    AuthorUpdate, 
    AuthorUpdateInternal, 
    AuthorDelete
)

class CRUDAuthor(FastCRUD[Author, AuthorCreateInternal, AuthorUpdate, AuthorUpdateInternal, AuthorDelete]):
    async def get_by_name(self, db: Session, *, first_name: str, last_name: str) -> Optional[Author]:
        return await db.query(self.model).filter(
            self.model.first_name == first_name,
            self.model.last_name == last_name
        ).first()

    async def get_with_quotes(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Author]:
        return await db.query(self.model).options(
            joinedload(self.model.quotes)
        ).offset(skip).limit(limit).all()

crud_authors = CRUDAuthor(AuthorsORM)