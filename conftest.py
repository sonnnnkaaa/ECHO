import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent))

if os.path.exists("test.db"):
    os.remove("test.db")

os.environ["DB_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "testsecretkey123456789"

from src.database import create_db_and_tables

create_db_and_tables()