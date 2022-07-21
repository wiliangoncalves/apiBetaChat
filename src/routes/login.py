from datetime import datetime, timedelta
from fastapi import FastAPI, status
from ..database.crud import get_user
from ..database.database import database_connect, database_disconnect, database

from jose import jwt

from decouple import config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256 as bcrypt


login_router = FastAPI()

class User(BaseModel):
    email: str | None = None
    password: str | None = None

@login_router.post("/")
async def login(users: User):
    await database_connect()

    query = "SELECT * FROM users WHERE email = :email"

    values = {"email": users.email}

    data = await get_user(query, values)

    # try:
    # decode_token = jwt.decode(encoded_token, 'MySECRET goes here', algorithms=['HS256'])
    # print("Token is still valid and active")
    # except jwt.ExpiredSignatureError:
    #     print("Token expired. Get new one")
    # except jwt.InvalidTokenError:
    #     print("Invalid Token")

    if data == None:
        return {
            'message': 'E-mail not found!',
            'status': status.HTTP_401_UNAUTHORIZED
        }

    token = {"token": data["id"]}

    token_encoded = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)

    hashPassword = bcrypt.verify(users.password, data["password"])

    if hashPassword and data != None:
        return {
            'message': 'Success!',
            'status': status.HTTP_200_OK,
            'token': token_encoded
        }

    if data["password"] != hashPassword:
        return {
            'message': 'Invalid password!',
            'status': status.HTTP_401_UNAUTHORIZED
        }
