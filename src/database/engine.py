from sqlalchemy import create_engine
from src.db_models import Base
from src.core import settings


DB_URL = settings.DB_URL
engine = create_engine(DB_URL, echo=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)