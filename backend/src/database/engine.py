from sqlalchemy import create_engine
from models import *
from config import Config


DB_URL = Config.DB_URL
engine = create_engine(DB_URL, echo=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)