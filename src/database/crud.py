from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .database import database, database_connect
import json

async def get_user(query, values):
    await database_connect()

    data = await database.fetch_all(query=query, values=values)

    if len(data) == 0:
        return None
    
    for items in data:
        item = dict(items)

    # convert_items_json = json.dumps(item, sort_keys=True)
    # show_items_json = json.loads(convert_items_json)

    return item

async def set_user(query, values):
    await database_connect()
    data = await database.execute_many(query=query, values=values)

    return data


async def get_community(query, values):
    await database_connect()

    data = await database.fetch_all(query=query, values=values)

    if len(data) == 0:
        return None

    community_list = []

    i = 0

    while i < len(data):
        community_list.append(dict(data[i]))

        if i >= len(data) - 1:
            break

        i += 1

    return community_list
