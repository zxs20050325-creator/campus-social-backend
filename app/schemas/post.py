from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import UserResponse


class PostBase(BaseModel):
    title: str
    content: str
    image_urls: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_urls: Optional[str] = None


class PostInDB(PostBase):
    id: int
    author_id: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostInDB):
    author: UserResponse


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentInDB(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentResponse(CommentInDB):
    author: UserResponse