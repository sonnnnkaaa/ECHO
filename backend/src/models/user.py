from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import TIMESTAMP, func
from typing import Optional
from datetime import datetime
from .base import Base


class User(Base):
    """
    Class for the "user" table.

    Columns:
        id: Post identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        username: Username (UNIQUE, NOT NULL)
        created_at: Date and time of account creation (NOT NULL)
        email: User's email (NOT NULL)
        avatar_url: User's avatar URL (OPTIONAL)
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    email: Mapped[str] = mapped_column(String(), unique=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String())