from sqlalchemy.orm import sessionmaker
from .engine import engine


Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()