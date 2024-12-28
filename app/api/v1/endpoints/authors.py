from fastapi import APIRouter#, Depends, HTTPException
#from fastapi.responses import JSONResponse
#from sqlalchemy.orm import Session
#from db.database import get_db
#from fastcrud import FastCRUD

#from db.models.author_orm_model import AuthorsORM
#from schemas.author import Author, AuthorCreateInternal, AuthorUpdate, AuthorDelete, AuthorUpdateInternal


router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("/test")  # этот путь будет доступен как /v1/authors/test
async def hello_world():
    return {"message": "Привет, мир!"}
# CRUDAuthor = FastCRUD[Author, AuthorCreateInternal, AuthorUpdate, AuthorUpdateInternal, AuthorDelete]
# crud_authors = CRUDAuthor(AuthorsORM)


# @router.post("/", response_model=Author)
# async def create_author(author_create: AuthorCreateInternal, db: Session = Depends(get_db)):
#     return await crud_authors.create(author_create, db)

# @router.get("/{author_id}", response_model=Author)
# async def read_author(author_id: int, db: Session = Depends(get_db)):
#     author = await crud_authors.get(author_id, db)
#     if author is None:
#         raise HTTPException(status_code=404, detail="Author not found")
#     return author

# @router.put("/{author_id}", response_model=Author)
# async def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
#     author = await crud_authors.update(author_id, author_update, db)
#     if author is None:
#         raise HTTPException(status_code=404, detail="Author not found")
#     return author

# @router.delete("/{author_id}", response_model=AuthorDelete)
# async def delete_author(author_id: int, db: Session = Depends(get_db)):
#     deleted_author = await crud_authors.delete(author_id, db)
#     if deleted_author is None:
#         raise HTTPException(status_code=404, detail="Author not found")
#     return JSONResponse(status_code=204, content={"message": "Author deleted successfully!"})

# @router.get("/", response_model=list[Author])
# async def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return await crud_authors.get_all(skip=skip, limit=limit, db)
