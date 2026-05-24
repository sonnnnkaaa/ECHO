from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, func
from datetime import datetime
from typing import List
from .checklist import Checklist
from .base import Base


class ChecklistCategory(Base):
    """
    Class for the "checklist_category" table.

    Columns:
        id: Checklist category identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        title: Checklist category title (UNIQUE, NOT NULL)
    """
    __tablename__ = "checklist_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    checklists: Mapped[List["Checklist"]] = relationship(
        secondary="checklist_checklist_category",
        back_populates="categories"
    )
