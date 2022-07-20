from fastapi import FastAPI, status
from ..database.crud import get_community
from ..database.database import database_connect
from pydantic import BaseModel

community_router = FastAPI()

class Community(BaseModel):
    id: int | None = None
    description: str | None = None

# @community_router.get("/")
# async def check_community():
    # await database_connect()

    # query = "SELECT * FROM"

    # values = {"pk": "communitys"}

    # data = await get_communitys(query, values)

    # print(data)

@community_router.post("/")
async def create_community(community: Community):
    await database_connect()

    query = "SELECT * FROM communitys WHERE id = :id"

    values = {"id": 1}

    data = await get_community(query, values)

    if data == None:
        return {
            'message': 'Success!',
            'status': status.HTTP_200_OK,
            'name': data["name"]
        }

    if data != None:
        return {
            'message': 'Name already exists!',
            'status': status.HTTP_406_NOT_ACCEPTABLE,
        }
