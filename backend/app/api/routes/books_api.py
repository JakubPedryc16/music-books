from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from app.api.dependencies import get_book_service
from app.db.db_async import get_async_session
from app.schemas.book_schema import BookData, BookPageData, BookPageResponse, BookResponse, UploadBookResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logger import logger

router = APIRouter(prefix="/books")


@router.get("/all", response_model=BookResponse)
async def get_all_books_api(
    session: AsyncSession = Depends(get_async_session)
) -> BookResponse:
    book_service = await get_book_service()
    try:
        books = await book_service.get_all(session=session)
        data = [
            BookData(
                id=book.id,
                title=book.title or "",
                author=book.author or "",
            )
            for book in books
        ]
        return BookResponse(success=True, data=data, error=None)
    except Exception as e:
        logger.error(f"Failed to fetch all books: {e}")
        return BookResponse(success=False, data=None, error=str(e))
    

@router.get("/page", response_model=BookPageResponse)
async def get_page_api(
    book_id: int = Query(...),
    page: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session)
) -> BookPageResponse:
    book_service = await get_book_service()
    try:
        result = await book_service.get_page(book_id=book_id, page=page, session=session)

        page_data = BookPageData(id=book_id, page=page, text=result)
        return BookPageResponse(success=True, data=page_data, error=None)
    except Exception as e:
        logger.error(f"Failed to fetch page {page} for book {book_id}: {e}")
        return BookPageResponse(success=False, data=None, error=str(e))

@router.post("/upload", response_model=UploadBookResponse)
async def add_book_api(
    book: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    book_service = await get_book_service()
    try:
        new_book = await book_service.add_book(
            pdf_file=book,
            title=title,
            author=author,
            session=session
        )

        return UploadBookResponse(success=True, data=new_book.id, error=None)
    except Exception as e:
        logger.error(f"Failed to upload book: {e}")
        return UploadBookResponse(success=False, data=None, error=str(e))
