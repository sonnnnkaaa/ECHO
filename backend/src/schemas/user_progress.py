from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List


class UserProgressCreate(BaseModel):
    pass #что тут вообще можно создать???


class UserProgressResponse(BaseModel):
    id: int
    user_id: int # нужен ли здесь юзер
    user_name: str
    item_id: int
    item_name: str
    post_id: int
    post_url: AnyUrl
    checklist_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None


class UserProgressListResponse(BaseModel):
    user_progress_list: List["UserProgressResponse"]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool
    