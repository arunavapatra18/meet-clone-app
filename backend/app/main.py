from fastapi import FastAPI

from app.core.auth import auth_router
from app.core.db import init_db
from app.models import User
from app.user.router import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    init_db()
