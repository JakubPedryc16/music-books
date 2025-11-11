import asyncio
import os
import aiofiles
from fpdf import FPDF
from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from app.db.db_async import AsyncSessionLocal
from app.models.book import Book
from app.utils.logger import logger

TXT_DIR = "data/books/txt/"
PDF_DIR = "data/books/pdf/"
FONT_PATH = "data/books/DejaVuSans.ttf"

def txt_to_pdf(txt_path: str, pdf_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    with open(txt_path, "r", encoding="utf-8-sig") as f: 
        for line in f:
            line = line.strip()
            if line:
                pdf.multi_cell(0, 5, line)

    pdf.output(pdf_path)

async def load_books_txt_pdf():
    os.makedirs(TXT_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)

    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Book).where((Book.file_name == None) | (Book.file_name == ""))
            )
            books = result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching books: {e}")
            return

    import httpx
    async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
        for book in books:
            if not book.link.lower().startswith("http"):
                logger.warning(f"Invalid link, skipping: {book.link}")
                continue

            txt_filename = f"{book.id}.txt"
            txt_path = os.path.join(TXT_DIR, txt_filename)

            try:
                response = await client.get(book.link)
                response.raise_for_status()
                async with aiofiles.open(txt_path, "wb") as f:
                    await f.write(response.content)
            except Exception as e:
                logger.error(f"Failed to download TXT: {book.title} ({book.link}) EXCEPTION={e}")
                continue

            pdf_filename = f"{book.id}.pdf"
            pdf_path = os.path.join(PDF_DIR, pdf_filename)
            try:
                txt_to_pdf(txt_path, pdf_path)
            except Exception as e:
                logger.error(f"Failed to convert TXT to PDF: {txt_path} EXCEPTION={e}")
                continue
            try:
                async with AsyncSessionLocal() as session:
                    await session.execute(
                        update(Book)
                        .where(Book.id == book.id)
                        .values(file_name=pdf_filename)
                    )
                    await session.commit()
            except SQLAlchemyError as e:
                logger.error(f"Failed to update database for book: {book.title} EXCEPTION={e}")
                continue

            logger.info(f"✅ Downloaded TXT and generated PDF for: {book.title} (ID={book.id})")

if __name__ == "__main__":
    asyncio.run(load_books_txt_pdf())
