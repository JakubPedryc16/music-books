import asyncio
import os
import aiofiles
import httpx
from sqlalchemy import update
from sqlalchemy.future import select
from app.db.db_async import AsyncSessionLocal
from app.models.book import Book
from app.utils.logger import logger

TEXT_DIR = "data/books/files/"

async def load_book_test():
    os.makedirs(TEXT_DIR, exist_ok=True)    

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Book).where((Book.file_name == None) | (Book.file_name == ""))
        )
        books = result.scalars().all()

    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        for book in books:
            file_url = book.link
            try:
                file_data = await client.get(file_url)
                file_data.raise_for_status()
            except Exception as exception:
                logger.error(f"Exception while downloading book txt file: TITLE={book.title} ID={book.id} EXCEPTION={exception}")
                continue  

            filename = f"{book.id}.txt"
            file_path = os.path.join(TEXT_DIR, filename)
            try: 
                async with aiofiles.open(file_path, "wb") as file:
                    await file.write(file_data.content) 
            except Exception as exception:
                logger.error(f"Exception while saving the downloaded book txt file: PATH={file_path} TITLE={book.title} ID={book.id} EXCEPTION={exception}")
                continue  

            async with AsyncSessionLocal() as session:
                await session.execute(
                    update(Book)
                    .where(Book.id == book.id)
                    .values(file_name=filename)
                )
                await session.commit()
                logger.info(f"Successfully downloaded and saved: {filename}")

if __name__ == "__main__":
    asyncio.run(load_book_test())
