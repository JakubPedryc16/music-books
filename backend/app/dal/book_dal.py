from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.DataAccessException import DataAccessException
from app.models.book import Book
from app.utils.logger import logger
from PyPDF2 import PdfReader
import shutil
from pathlib import Path
import uuid

BOOK_STORAGE_PATH = Path("data/books/pdf/")

class BookDAL:
    def __init__(self):
        pass

    async def get_all(self, session: AsyncSession) -> list[Book]:
        try:
            query = select(Book)
            result = await session.scalars(query)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all: {e}")
            raise DataAccessException("Failed to fetch all books")

    async def get_book_by_id(self, book_id: int, session: AsyncSession) -> Book | None:
        try:
            query = select(Book).where(Book.id == book_id)
            result = await session.scalar(query)
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_book_by_id: {e}")
            raise DataAccessException(f"Failed to fetch book {book_id}")

    async def add_book(self, pdf_file: UploadFile, title: str, author: str, session: AsyncSession) -> Book:
        try:
            BOOK_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
            filename = f"{uuid.uuid4()}.pdf"
            file_path = BOOK_STORAGE_PATH / filename

            with file_path.open("wb") as f:
                shutil.copyfileobj(pdf_file.file, f)

            new_book = Book(file_name=filename, title=title, author=author)
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book

        except Exception as e:
            logger.error(f"Error adding book: {e}")
            raise DataAccessException("Failed to add book")

    async def get_pages(self, book_id: int, pages: list[int], session: AsyncSession) -> dict[int, str]:
        try:
            if len(pages) == 1 and isinstance(pages[0], list):
                pages = pages[0]

            book = await self.get_book_by_id(book_id, session)
            if not book:
                return {}

            if not book.file_name:
                raise DataAccessException(f"Book {book_id} has no file_name set")

            pdf_path = BOOK_STORAGE_PATH / book.file_name
            if not pdf_path.exists():
                raise DataAccessException(f"PDF file for book {book_id} not found")

            reader = PdfReader(str(pdf_path))
            result = {}
            for page_num in pages:
                if 1 <= page_num <= len(reader.pages):
                    text = reader.pages[page_num - 1].extract_text() or ""
                    if text.strip():
                        result[page_num] = text.strip()
                else:
                    result[page_num] = "[Page out of range]"
            return result

        except Exception as e:
            logger.error(f"Error reading pages: {e}")
            raise DataAccessException(f"Failed to read pages for book {book_id}")
