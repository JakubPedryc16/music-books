import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  
    yield             


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "SQLite is connected"}

