from fastapi import FastAPI, status, Request
from ..database.crud import get_community
from ..database.database import database_connect
from pydantic import BaseModel
import collections

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

    values = {"tk": decoded_token["token"]}

    # query = "select * from community_users inner join users on users_id = :tk join communitys on communitys_id = communitys.id"

    # query = "select * from communitys, users, community_users  where users.id = :tk and :tk = community_users.users_id and communitys.id = communitys_id"

    query = "select community_name, community_avatar from communitys, users, community_users where users.id = :tk and :tk = community_users.users_id and communitys.id = communitys_id"

    data = await get_community(query, values)

    if data == None:
            return {
                'message': 'None community was found!',
                'status': status.HTTP_404_NOT_FOUND
            }
    else:
        return {
            'message': 'Community found!',
            'status': status.HTTP_200_OK,
            'data': data
        }
