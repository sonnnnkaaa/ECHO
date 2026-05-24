from sqlalchemy.orm import sessionmaker
from .engine import engine


SessionLocal = sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()