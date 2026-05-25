from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List
from .checklist_item import ChecklistItemResponse
from .checklist_category import ChecklistCategoryResponse


class ChecklistCreate(BaseModel):
    title: str
    description: str
    image_url: Optional[AnyUrl] = None
    categories: List[str] = []


class ChecklistResponse(BaseModel):
    id: int
    title: str
    categories: List[ChecklistCategoryResponse]
    description: str
    image_url: Optional[AnyUrl]
    author_id: int
    saves_count: int
    created_at: datetime
    class Config:
        from_attributes = True

class ChecklistUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[AnyUrl] = None
    categories: Optional[List[str]] = None


class ChecklistListResponse(BaseModel):
    checklists: List[ChecklistResponse]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool
