from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int
    author_name: str
    author_avatar: Optional[AnyUrl] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool
