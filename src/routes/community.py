from fastapi import FastAPI, status, Request
from ..database.crud import get_community
from ..database.database import database_connect
from pydantic import BaseModel

from jose import jwt

from decouple import config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

community_router = FastAPI()

@community_router.get("/")
async def create_community(request: Request):
    await database_connect()

    token = request.headers.get('Authorization').split(" ")[-1]

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    query = "select * from community_users inner join users on users_id = :tk join communitys on communitys_id = communitys.id"

    values = {"tk": decoded_token["token"]}

    data = await get_community(query, values)

    print('COMMUNITY', data)

    return {
        'message': 'Chegou no community'
    }

    # query = "SELECT * FROM communitys WHERE id = :id"

    # values = {"id": 1}

    # data = await get_community(query, values)

    # if data == None:
    #     return {
    #         'message': 'Success!',
    #         'status': status.HTTP_200_OK,
    #         'name': data["name"]
    #     }

    # if data != None:
    #     return {
    #         'message': 'Name already exists!',
    #         'status': status.HTTP_406_NOT_ACCEPTABLE,
    #     }
