from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    text: str
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentListResponse(BaseModel):
    comments: List["CommentResponse"]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool
