from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, func, ForeignKey
from typing import Optional, List
from datetime import datetime
from .base import Base

class Checklist(Base):
    """
    Class for the "checklist" table.

    Columns:
        id: Checklist identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        title: Checklist title (UNIQUE, NOT NULL)
        saves_count: Number of checklist saves (NOT NULL)
        created_at: Date and time of checklist creation (NOT NULL)
        description: Checklist description (OPTIONAL)
        author_id: Checklist author identifier (FOREIGN KEY user(id), NOT NULL)
        checklist_checklist_category_id: Identifier of the checklist and category connection (FOREIGN KEY checklist_checklist_category(id), NOT NULL)
    """
    __tablename__ = "checklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    saves_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    description: Mapped[Optional[str]] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    categories: Mapped[List["ChecklistCategory"]] = relationship(
        secondary="checklist_checklist_category",
        back_populates="checklists")
    
