from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class ChecklistChecklistCategory(Base):
    """
    Class for the "checklist_checklist_category" table.

    Columns:
        id: Identifier of the checklist and category connection (PRIMARY KEY, UNIQUE, NOT NULL)
        checklist_id: Checklist identifier (NOT NULL)
        checklist_category_id: Checklist category identifier (NOT NULL)
    """
    __tablename__ = "checklist_checklist_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    checklist_id: Mapped[int] = mapped_column(ForeignKey("checklist.id"))
    checklist_category_id: Mapped[int] = mapped_column(ForeignKey("checklist_category.id"))