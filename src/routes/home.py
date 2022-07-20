import json
from fastapi import FastAPI
from ..database.database import database_connect
from ..database.crud import get_user
from pydantic import BaseModel

from jose import jwt

from decouple import config
SECRET_KEY = config('SECRET_KEY')

class Token(BaseModel):
    token: str | None = None

home_router = FastAPI()

@home_router.post("/")
async def home(token: Token):
    await database_connect()
    decoded_token = jwt.decode(token.token, SECRET_KEY, algorithms=['HS256'])

    query = "SELECT * FROM users WHERE id = :tk"

    values = {"tk": decoded_token["token"]}

    data = await get_user(query, values)

    print(data['email'])

    return {
        'message': 'Chegou',
        'name': data['name'],
        'email': data['email']
    }
