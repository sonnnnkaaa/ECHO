from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChecklistCategoryCreate(BaseModel):
    title: str


class ChecklistCategoryResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class ChecklistCategoryUpdate(BaseModel):
    title: str