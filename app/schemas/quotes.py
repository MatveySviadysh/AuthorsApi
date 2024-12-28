from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class QuoteBase(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="Текст цитаты"
    )
    year: Optional[int] = Field(
        None, 
        ge=0, 
        le=datetime.now().year,
        description="Год создания цитаты"
    )
    source: Optional[str] = Field(
        None, 
        max_length=255,
        description="Источник цитаты"
    )
    author_id: int = Field(
        ..., 
        gt=0,
        description="ID автора цитаты"
    )

class QuoteCreate(QuoteBase):
    pass

class QuoteCreateInternal(QuoteCreate):
    pass

class QuoteUpdate(BaseModel):
    text: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=1000,
        description="Текст цитаты"
    )
    year: Optional[int] = Field(
        None, 
        ge=0, 
        le=datetime.now().year,
        description="Год создания цитаты"
    )
    source: Optional[str] = Field(
        None, 
        max_length=255,
        description="Источник цитаты"
    )
    author_id: Optional[int] = Field(
        None, 
        gt=0,
        description="ID автора цитаты"
    )

class QuoteUpdateInternal(QuoteUpdate):
    pass

class Quote(QuoteBase):
    id: int = Field(description="Уникальный идентификатор цитаты")
    created_at: datetime = Field(description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")

    model_config = ConfigDict(from_attributes=True)

class QuoteDelete(BaseModel):
    id: int = Field(description="ID удаляемой цитаты")
    is_deleted: bool = Field(default=True, description="Флаг удаления")
    deleted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Дата удаления"
    )
