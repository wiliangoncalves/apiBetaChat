from fastapi import FastAPI
from databases import Database

from decouple import config
DATABASE_URL = config('DATABASE_URL')
database = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


# database = Database("sqlite:///betachat")
