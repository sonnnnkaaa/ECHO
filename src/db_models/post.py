from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from .base import Base


class Post(Base):
    """
    Class for the "post" table.

    Columns:
        id: Post identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        image_url: URL of the image attached to the post (NOT NULL)
        description: Post description (OPTIONAL)
        likes_count: Number of likes (NOT NULL)
        comments_count: Number of comments (NOT NULL)
        created_at: Date and time of post creation (NOT NULL)
        user_id: Identifier of the user who posted (FOREIGN KEY user(id), NOT NULL)
        item_id: Identifier of the checklist item the post is dedicated to (FOREIGN KEY checkilst_item(id), NOT NULL)
    """
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("checklist_item.id"))