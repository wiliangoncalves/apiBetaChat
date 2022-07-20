from fastapi import FastAPI, status
from ..database.crud import get_user, set_user
from ..database.database import database_connect, database_disconnect

from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256 as bcrypt
import re

register_router = FastAPI()

class User(BaseModel):
    name: str | None = None
    username: str | None = None
    email: str
    password: str
    repeat_password: str


@register_router.post("/")
async def set_register(users: User):
    await database_connect()
 
    query = "SELECT * FROM users WHERE email = :email"

    values = {"email": users.email}

    database_check_email  = await get_user(query, values)

    hash_password = bcrypt.hash(users.password)

    if users.name.strip() == '':
        return {
            'message': 'Please fill out Name',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    if users.name[0].isdigit():
        return {
            'message': 'Name does not initiate with Numeric.',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    if users.username.strip() == '':
        return {
            'message': 'Please fill out Username',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    """ Check E-mail pattern """
    def solve(email):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat,email):
            return True
        return False

    email = users.email

    if solve(email) == False:
        return {
            'message': 'Invalid email address',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }


    if users.email.strip() == '':
        return {
            'message': 'Please fill out E-mail',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    if database_check_email != None:
        return {
            'message': 'E-mail is already registered!',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    if users.password != users.repeat_password:
        return {
            'message': 'The password is incorrect. Try again',
            'status': status.HTTP_406_NOT_ACCEPTABLE
        }

    query = "INSERT INTO users(name, username, password, email) VALUES (:name, :username, :password, :email)"
    
    values = [
        {"name": users.name, "username": users.username, "password": hash_password, "email": users.email},
    ]
    await set_user(query, values)

    return {
        'message': 'Success!',
        'status': status.HTTP_200_OK
    }
