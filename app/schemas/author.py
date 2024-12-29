from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=50)
    birth_date: datetime
    death_date: Optional[datetime] = None
    bio: Optional[str] = Field(None, max_length=1000)
    photo: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorCreateInternal(AuthorCreate):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50) 
    patronymic: Optional[str] = Field(None, min_length=2, max_length=50)
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    bio: Optional[str] = Field(None, max_length=1000)
    photo: Optional[str] = None

class AuthorUpdateInternal(AuthorUpdate):
    pass

class Author(AuthorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AuthorDelete(BaseModel):
    id: int
    is_deleted: bool = True
    deleted_at: datetime = Field(default_factory=datetime.utcnow)