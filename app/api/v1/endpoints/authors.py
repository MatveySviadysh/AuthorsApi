from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.author import Author, AuthorCreateInternal, AuthorUpdate, AuthorUpdateInternal, AuthorDelete
from db.session import get_db
from crud.crud_author import crud_authors


router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)


@router.post("/", response_model=Author)
async def create_author(author_create: AuthorCreateInternal, db: Session = Depends(get_db)):
    return await crud_authors.create(db=db, obj_in=author_create)

@router.get("/{author_id}", response_model=Author)
async def read_author(author_id: int, db: Session = Depends(get_db)):
    author = await crud_authors.get(db=db, id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=Author)
async def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    author = await crud_authors.get(db=db, id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return await crud_authors.update(db=db, db_obj=author, obj_in=author_update)

@router.delete("/{author_id}", response_model=AuthorDelete)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_author = await crud_authors.delete(db=db, id=author_id)
    if deleted_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return deleted_author

@router.get("/", response_model=List[Author])
async def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await crud_authors.get_all(db=db, skip=skip, limit=limit)

@router.get("/all/", response_model=List[Author])
async def get_all_authors(db: Session = Depends(get_db)):
    authors = await crud_authors.get_all(db=db, skip=0, limit=None)
    if not authors:
        raise HTTPException(status_code=404, detail="Авторы не найдены")
    return authors
