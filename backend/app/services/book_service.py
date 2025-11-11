from app.dal.book_dal import BookDAL
from app.models.book import Book
from sqlalchemy.ext.asyncio import AsyncSession

class BookService:
    def __init__(self):
        pass

    async def get_all(self, session: AsyncSession) -> list[Book]:
        book_dal = BookDAL()
        return await book_dal.get_all(session=session)

    async def add_book(self, pdf_file, title: str, author: str, session: AsyncSession) -> Book:
        book_dal = BookDAL()
        return await book_dal.add_book(pdf_file, title=title, author=author, session=session)

    async def get_page(self, book_id: int, page: int, session: AsyncSession) -> str:
        book_dal = BookDAL()
        pages = await book_dal.get_pages(book_id, [page], session=session)
        return pages.get(page, "")
