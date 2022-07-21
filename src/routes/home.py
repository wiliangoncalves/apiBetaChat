import json
from fastapi import FastAPI, Request
from flask import jsonify
from ..database.database import database_connect
from ..database.crud import get_user
from pydantic import BaseModel

from jose import jwt

from decouple import config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class Token(BaseModel):
    token: str | None = None

home_router = FastAPI()

@home_router.get("/")
async def home(request: Request):
    await database_connect()

    token = request.headers.get('Authorization').split(" ")[-1]

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    query = "SELECT * FROM users WHERE id = :tk"

    values = {"tk": decoded_token["token"]}

    data = await get_user(query, values)

    return {
        'message': 'Chegou',
        'name': data['name'],
        'email': data['email'],
        'avatar': data['avatar']
    }
