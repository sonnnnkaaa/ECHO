from pydantic import BaseModel
from datetime import datetime
from typing import List


class FavoriteCreate(BaseModel):
    pass


class FavoriteListResponse(BaseModel):
    id: int
    user_id: int
    user_name: str # кто сохранил
    checklist_id: List[int]
    checklist_title: List[str]
    created_at: datetime
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool # здесь подумать надо ли вообще эта конструкция