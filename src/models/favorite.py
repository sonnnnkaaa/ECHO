from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from datetime import datetime
from .base import Base


class Favorite(Base):
    """
    Class for the "favorite" table.

    Columns:
        id: Save to Favorites identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        created_at: Date and time of save to Favorites (NOT NULL)
        user_id: Identifier of the user who saved the checklist (FOREIGN KEY user(id), NOT NULL)
        checklist_id: Saved checklist identifier (FOREIGN KEY checklist(id), NOT NULL)
    """
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    checklist_id: Mapped[int] = mapped_column(ForeignKey("Checklist.id"))
    