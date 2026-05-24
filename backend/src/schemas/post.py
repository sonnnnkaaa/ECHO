from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List


class PostCreate(BaseModel):
    description: str
    image_url: AnyUrl


class PostResponse(BaseModel):
    id: int
    image_url: AnyUrl
    item_id: int
    item_name: str
    checklist_id: int
    checklist_name: str
    author_id: int
    author_name: str
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class PostUpdate(BaseModel):
    description: Optional[str] = None


class PostListResponse(BaseModel):
    posts: List["PostResponse"]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool


