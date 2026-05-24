from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class ChecklistItem(Base):
    """
    Class for the "checklist_item" table.

    Columns:
        id: Checklist item identifier (PRIMARY KEY, UNIQUE, NOT NULL)
        description: Checklist item description (NOT NULL)
        order_number: Order number of the item in the checklist (NOT NULL)
        checklist_id: Checklist identifier (FOREIGN KEY checklist(id), NOT NULL)
    """
    __tablename__ = "checklist_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    order_number: Mapped[int] = mapped_column()
    checklist_id: Mapped[int] = mapped_column(ForeignKey("checklist.id")) 