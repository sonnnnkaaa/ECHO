from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
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