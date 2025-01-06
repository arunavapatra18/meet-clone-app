from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.auth import auth_router
from app.core.db import init_db
from app.models import User
from app.user.router import user_router
from app.webrtc.signaling_server import SignalingServer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers=['*']
)

app.include_router(auth_router)
app.include_router(user_router)

signaling_server = SignalingServer(app)

@app.on_event("startup")
def on_startup():
    init_db()
