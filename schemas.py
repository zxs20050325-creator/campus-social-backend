from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# 用户相关Schema
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = ""


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    is_active: Optional[bool] = True


class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 资源置换相关Schema
class ExchangeBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = "良好"
    image_urls: Optional[str] = None
    is_available: bool = True


class ExchangeCreate(ExchangeBase):
    owner_id: int


class ExchangeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    image_urls: Optional[str] = None
    is_available: Optional[bool] = None


class ExchangeResponse(ExchangeBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 社交帖子相关Schema
class PostBase(BaseModel):
    title: str
    content: str
    image_urls: Optional[str] = None


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_urls: Optional[str] = None


class PostResponse(PostBase):
    id: int
    author_id: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 评论相关Schema
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int
    author_id: int


class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True