from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import List


class LikeCreate(BaseModel):
    pass


class LikeResponse(BaseModel):
    id: int
    post_id: int
    post_url: AnyUrl
    author_name: str
    created_at: datetime


class LikeListResponse(BaseModel):
    likes: List["LikeListResponse"] 
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool