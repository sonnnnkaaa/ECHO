from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List


class PostCreate(BaseModel):
    description: str
    image_url: AnyUrl
    item_id: int


class PostResponse(BaseModel):
    id: int
    image_url: AnyUrl
    item_id: int
    user_id: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    description: Optional[str] = None


class PostListResponse(BaseModel):
    posts: List["PostResponse"]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool


