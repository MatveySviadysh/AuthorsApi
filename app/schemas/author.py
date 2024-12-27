from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class Author(AuthorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 