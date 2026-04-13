from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from datetime import datetime
from .base import Base


class Comment(Base):
    """
    Class for the "comment" table.

    Columns:
        id: Comment identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        text: Comment content (NOT NULL)
        created_at: Date and time of comment creation (NOT NULL)
        post_id: Post on which the comment was left (FOREIGN KEY post(id), NOT NULL)
        author_id: Checklist author identifier (FOREIGN KEY user(id), NOT NULL)
    """
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("User.id"))