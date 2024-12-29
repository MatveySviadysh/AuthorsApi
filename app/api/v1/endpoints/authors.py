from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from schemas.author import Author, AuthorCreateInternal, AuthorUpdate, AuthorDelete
from db.session import get_db
from crud.crud_author import crud_authors
from services.redis.cache import _invalidate_cache, _set_author_cache, redis_client

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.post("/", response_model=Author, 
    summary="Создать нового автора",
    description="Создает нового автора в базе данных и возвращает его данные",
    response_description="Созданный автор")
async def create_author(
    author_create: AuthorCreateInternal, 
    db: Session = Depends(get_db)
):
    author = await crud_authors.create(db=db, obj_in=author_create)
    await _invalidate_cache([f"author:{author.id}", "authors:all"])
    await _set_author_cache(author)
    return author


@router.get("/{author_id}", response_model=Author,
    summary="Получить автора по ID",
    description="Возвращает информацию об авторе по его идентификатору",
    response_description="Данные автора")
async def read_author(
    author_id: int, 
    db: Session = Depends(get_db)
):
    cache_key = f"author:{author_id}"
    if cached_author := await redis_client.get(cache_key):
        return json.loads(cached_author)
    
    if author := await crud_authors.get(db=db, id=author_id):
        await _set_author_cache(author)
        return author
    raise HTTPException(status_code=404, detail="Автор не найден")


@router.put("/{author_id}", response_model=Author,
    summary="Обновить данные автора",
    description="Обновляет информацию об авторе по его идентификатору",
    response_description="Обновленные данные автора")
async def update_author(
    author_id: int, 
    author_update: AuthorUpdate, 
    db: Session = Depends(get_db)
):
    if not (author := await crud_authors.get(db=db, id=author_id)):
        raise HTTPException(status_code=404, detail="Автор не найден")
    
    updated_author = await crud_authors.update(db=db, db_obj=author, obj_in=author_update)
    cache_keys = [
        f"author:{author_id}",
        "authors:all",
        *[f"authors:list:{i}:10" for i in range(10)]
    ]
    await _invalidate_cache(cache_keys)
    await _set_author_cache(updated_author)
    return updated_author


@router.delete("/{author_id}", response_model=AuthorDelete,
    summary="Удалить автора",
    description="Удаляет автора по его идентификатору",
    response_description="Удаленный автор")
async def delete_author(
    author_id: int, 
    db: Session = Depends(get_db)
):
    if not (deleted_author := await crud_authors.delete(db=db, id=author_id)):
        raise HTTPException(status_code=404, detail="Автор не найден")
    
    cache_keys = [
        f"author:{author_id}",
        "authors:all",
        *[f"authors:list:{i}:10" for i in range(10)]
    ]
    await _invalidate_cache(cache_keys)
    return deleted_author


@router.get("/", response_model=List[Author],
    summary="Получить список авторов",
    description="Возвращает список авторов с пагинацией",
    response_description="Список авторов")
async def read_authors(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    cache_key = f"authors:list:{skip}:{limit}"
    if cached_authors := await redis_client.get(cache_key):
        return json.loads(cached_authors)
    
    if authors := await crud_authors.get_all(db=db, skip=skip, limit=limit):
        await redis_client.set(cache_key, json.dumps([author.to_dict() for author in authors]), ex=600)
        return authors
    return []


@router.get("/all/", response_model=List[Author],
    summary="Получить всех авторов",
    description="Возвращает полный список всех авторов",
    response_description="Полный список авторов")
async def get_all_authors(db: Session = Depends(get_db)):
    cache_key = "authors:all"
    if cached_authors := await redis_client.get(cache_key):
        return json.loads(cached_authors)
    
    if authors := await crud_authors.get_all(db=db, skip=0, limit=None):
        await redis_client.set(cache_key, json.dumps([author.to_dict() for author in authors]), ex=600)
        return authors
    raise HTTPException(status_code=404, detail="Авторы не найдены")
