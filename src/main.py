import sys
from pathlib import Path
from contextlib import asynccontextmanager
sys.path.insert(0, str(Path(__file__).parent.parent))
from fastapi import FastAPI
from src.api import auth, checklist_item, checklist, comment, favorite, like, post, user
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="App", version="1.0.0")

app.include_router(auth.router)
app.include_router(checklist_item.router)
app.include_router(checklist.router)
app.include_router(comment.router)
app.include_router(favorite.router)
app.include_router(like.router)
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome"}