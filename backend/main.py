from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError, ResponseValidationError
import requests

# Pobieranie paczek NLTK w buildzie
# RUN python -m nltk.downloader punkt averaged_perceptron_tagger

from app.api.dependencies import init_book_service, init_embedding_service, init_matchers
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import AsyncSessionLocal
from app.services.global_music_context import GlobalMusicContext
from app.utils import global_exception_handler
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException 

from app.db.init_db import init_db
from app.api.routes import books_api, match_api, spotify_api
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.utils.logger import logger
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    init_embedding_service()  

    context = GlobalMusicContext()
    
    async with AsyncSessionLocal() as session: 
            await context.initialize(session)

    init_matchers() 
    init_book_service()
    yield             

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(settings.FRONTEND_URL)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    logger.info(settings.FRONTEND_URL)
    return {"message": "SQLite is connected"}

app.include_router(spotify_api.router)
app.include_router(match_api.router)
app.include_router(books_api.router)

app.add_exception_handler(RequestValidationError, global_exception_handler.validation_exception_handler)
app.add_exception_handler(ResponseValidationError, global_exception_handler.response_validation_exception_handler)
app.add_exception_handler(HTTPException, global_exception_handler.http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler.unhandled_exception_handler)

