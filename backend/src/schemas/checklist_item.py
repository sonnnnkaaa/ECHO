from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ChecklistItemCreate(BaseModel):
    description: str


class ChecklistItemResponse(BaseModel):
    id: int
    description: str
    order_number: int
    checklist_id: int
    checklist_title: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ChecklistItemUpdate(BaseModel):
    description: str


class ChecklistItemListResponse(BaseModel):
    checklist_items: List["ChecklistItemResponse"]
    total: int
    page: int
    size: int
    has_prev: bool
    has_next: bool