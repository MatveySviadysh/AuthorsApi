from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from schemas.quotes import Quote, QuoteCreateInternal, QuoteUpdateInternal, QuoteDelete
from db.session import get_db
from crud.crud_quotes import crud_quotes
from services.redis.cache import _invalidate_cache, _set_author_cache, redis_client

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.get("/all", response_model=List[Quote],
    summary="Получить все цитаты",
    description="Возвращает полный список всех цитат",
    response_description="Полный список цитат")
async def get_all_quotes(db: Session = Depends(get_db)):
    cache_key = "quotes:all"
    if cached_quotes := await redis_client.get(cache_key):
        return json.loads(cached_quotes)

    quotes = await crud_quotes.get_all(db=db)
    await redis_client.set(cache_key, json.dumps([quote.to_dict() for quote in quotes]), ex=600)
    return quotes

@router.get("/{quote_id}", response_model=Quote,
    summary="Получить цитату по ID",
    description="Возвращает информацию о цитате по её идентификатору",
    response_description="Данные цитаты")
async def get_quote(quote_id: int, db: Session = Depends(get_db)):
    cache_key = f"quote:{quote_id}"
    if cached_quote := await redis_client.get(cache_key):
        return json.loads(cached_quote)

    quote = await crud_quotes.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Цитата не найдена")

    await redis_client.set(cache_key, json.dumps(quote.to_dict()), ex=600)
    return quote

@router.post("", response_model=Quote,
    summary="Создать новую цитату",
    description="Создает новую цитату в базе данных и возвращает её данные",
    response_description="Созданная цитата")
async def create_quote(quote: QuoteCreateInternal, db: Session = Depends(get_db)):
    new_quote = await crud_quotes.create(db=db, obj_in=quote)
    await _invalidate_cache([f"quote:{new_quote.id}"])
    await _set_author_cache(new_quote)
    return new_quote

@router.put("/{quote_id}", response_model=Quote,
    summary="Обновить цитату",
    description="Обновляет информацию о цитате по её идентификатору",
    response_description="Обновленные данные цитаты")
async def update_quote(quote_id: int, quote: QuoteUpdateInternal, db: Session = Depends(get_db)):
    existing_quote = await crud_quotes.get(db=db, id=quote_id)
    if not existing_quote:
        raise HTTPException(status_code=404, detail="Цитата не найдена")

    updated_quote = await crud_quotes.update(db=db, db_obj=existing_quote, obj_in=quote)
    await _invalidate_cache([f"quote:{quote_id}"])
    await _set_author_cache(updated_quote)
    return updated_quote

@router.delete("/{quote_id}", response_model=QuoteDelete,
    summary="Удалить цитату",
    description="Удаляет цитату по её идентификатору",
    response_description="Удаленная цитата")
async def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    existing_quote = await crud_quotes.get(db=db, id=quote_id)
    if not existing_quote:
        raise HTTPException(status_code=404, detail="Цитата не найдена")

    result = await crud_quotes.delete(db=db, id=quote_id)
    await _invalidate_cache([f"quote:{quote_id}"])
    return {"id": quote_id, "is_deleted": result.is_deleted}
