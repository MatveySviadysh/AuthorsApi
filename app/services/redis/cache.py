import json
from typing import List, Union, Any
from redis import asyncio as aioredis
from core.config import settings
from db.models.author_orm_model import AuthorsORM

redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

# Константы для TTL (Time To Live)
DEFAULT_TTL = 600  # 10 минут
LONG_TTL = 3600   # 1 час

async def _delete_hash(hash_key: str) -> None:
    """Удаляет хеш и все его поля"""
    await redis_client.delete(hash_key)

async def _invalidate_cache(keys: List[str]) -> None:
    """Инвалидация кеша для списка ключей"""
    if keys:
        await redis_client.delete(*keys)

async def _set_cache(key: str, data: Any, ttl: int = DEFAULT_TTL) -> None:
    """Универсальный метод установки кеша с TTL"""
    await redis_client.set(
        key,
        json.dumps(data) if not isinstance(data, str) else data,
        ex=ttl
    )

async def _get_cache(key: str) -> Union[dict, list, None]:
    """Универсальный метод получения данных из кеша"""
    if data := await redis_client.get(key):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    return None

async def _set_author_cache(author: AuthorsORM) -> None:
    """Установка кеша для автора"""
    await _set_cache(f"author:{author.id}", author.to_dict())

async def _set_authors_list_cache(
    authors: List[AuthorsORM],
    skip: int = 0,
    limit: int = 10
) -> None:
    """Установка кеша для списка авторов"""
    key = f"authors:list:{skip}:{limit}"
    await _set_cache(key, [author.to_dict() for author in authors])

async def _clear_all_author_caches() -> None:
    """Очистка всех кешей, связанных с авторами"""
    pattern = "author:*"
    keys = await redis_client.keys(pattern)
    if keys:
        await _invalidate_cache(keys)
