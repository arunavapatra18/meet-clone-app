from fastapi import FastAPI

from app.core.db import init_db
from app.models import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()
    