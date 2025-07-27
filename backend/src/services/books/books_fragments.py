import asyncio
import aiofiles
import chardet
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.book import Book
from src.models.book_fragment import BookFragment
from src.db.db_async import AsyncSessionLocal

from src.utils.logger import logger

BOOKS_PATH = "data/books/files/"

async def detect_encoding_async(filename: str) -> str:
    async with aiofiles.open(BOOKS_PATH + filename, 'rb') as f:
        rawdata = await f.read(10000)
    result = chardet.detect(rawdata)
    return result['encoding']


async def read_file(filename: str, encoding: str = 'utf-8') -> str:
    async with aiofiles.open(BOOKS_PATH + filename, 'r', encoding=encoding) as f:
        return await f.read()


async def split_fragments(text: str, words_per_fragment: int = 1000) -> list[str]:
    words = text.split()
    return [' '.join(words[i:i + words_per_fragment]) for i in range(0, len(words), words_per_fragment)]


async def create_fragments_for_books_without_them(words_per_fragment: int = 1000):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Book).options(selectinload(Book.fragments))
        )
        books = result.scalars().all()

        for book in books:
            if book.fragments:
                continue
            if not book.file_name:
                logger.error(f"Book {book.id} has no file_name")
                continue

            encoding = await detect_encoding_async(book.file_name)
            try:
                full_text = await read_file(book.file_name, encoding)
            except Exception as e:
                logger.error(f"Could not read book {book.id}: {e}")
                continue

            text_fragments = await split_fragments(full_text, words_per_fragment)

            fragment_list = [
                BookFragment(
                    book_id=book.id,
                    fragment_index=i,
                    embedding=None,
                    tag_embedding=None
                )
                for i in range(len(text_fragments))
            ]

            for fragment in fragment_list:
                session.add(fragment)

        await session.commit()
        logger.info("Fragments Succesfully updated")


if __name__ == "__main__":
    asyncio.run(create_fragments_for_books_without_them())
