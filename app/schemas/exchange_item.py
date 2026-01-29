from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import UserResponse


class ExchangeItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = "良好"
    image_urls: Optional[str] = None


class ExchangeItemCreate(ExchangeItemBase):
    pass


class ExchangeItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    image_urls: Optional[str] = None
    is_available: Optional[bool] = None


class ExchangeItemInDB(ExchangeItemBase):
    id: int
    owner_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExchangeItemResponse(ExchangeItemInDB):
    owner: UserResponse