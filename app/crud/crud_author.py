   
from fastcrud import FastCRUD

from db.models.author_orm_model import AuthorsORM
from schemas.author import Author, AuthorUpdate, AuthorCreateInternal, AuthorUpdateInternal, AuthorDelete

CRUDAuthor = FastCRUD[Author, AuthorCreateInternal, AuthorUpdate, AuthorUpdateInternal, AuthorDelete]
crud_authors = CRUDAuthor(AuthorsORM)