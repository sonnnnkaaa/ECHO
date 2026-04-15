from pydantic import BaseModel, EmailStr, AnyUrl
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    nickname: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    created_at: datetime
    is_active: bool
    avatar_url: Optional[AnyUrl] = None


# class UserUpdate(BaseModel):
    