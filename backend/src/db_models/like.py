from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from datetime import datetime
from .base import Base


class Like(Base):
    """
    Class for the "like" table.

    Columns:
        id: Like identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        created_at: Date and time of like creation (NOT NULL)
        post_id: Identifier of the post that was liked (FOREIGN KEY post(id), NOT NULL)
        user_id: Identifier of the user who liked (FOREIGN KEY user(id), NOT NULL)
    """
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))