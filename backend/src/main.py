import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))


from fastapi import FastAPI
from src.api import auth, user

app = FastAPI(title="App", version="1.0.0")

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome"}