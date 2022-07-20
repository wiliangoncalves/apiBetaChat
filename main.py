from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.database import crud
from src.database import database
from src.routes.register import register_router
from src.routes.login import login_router
from src.routes.community import community_router
from src.routes.home import home_router
import uvicorn

app = FastAPI()
app.mount("/register", register_router)
app.mount("/login", login_router)
app.mount("/community", community_router)
app.mount("/home", home_router)