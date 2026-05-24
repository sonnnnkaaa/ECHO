from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional, List
from .checklist_item import ChecklistItemResponse
from .checklist_category import ChecklistCategoryResponse


class ChecklistCreate(BaseModel):
    title: str
    description: str
    image_url: Optional[AnyUrl]


class ChecklistResponse(BaseModel):
    id: int
    title: str
    categories: List[str]
    description: str
    image_url: Optional[AnyUrl]
    author_id: int
    author_name: str
    saves_count: int
    items: List["ChecklistItemResponse"] # когда будет дописан класс 
    created_at: datetime
    updated_at: Optional[datetime]

class ChecklistUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[AnyUrl] = None
    categories: Optional[List["ChecklistCategoryResponse"]] = None


class ChecklistListResponse(BaseModel):
    checklists: List[str]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool