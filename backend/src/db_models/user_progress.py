from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from .base import Base


class UserProgress(Base):
    """
    Class for the "user_progress" table.

    Columns:
        id: Post identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        is_completed: Completed or not (NOT NULL)
        completed_at: Date and time of completion
        user_id: Identifier of the user who completed the checklist item (FOREIGN KEY user(id), NOT NULL)
        item_id: Identifier of the completed checklist item (FOREIGN KEY checkilst_item(id), NOT NULL)
        post_id: Linked post identifier (FOREIGN KEY post(id), NOT NULL)
    """
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_completed: Mapped[bool] = mapped_column()
    completed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("checklist_item.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))