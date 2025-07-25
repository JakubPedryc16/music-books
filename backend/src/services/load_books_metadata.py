import asyncio
import httpx
from sqlalchemy import select
from src.db.db_async import AsyncSessionLocal
from src.models.book import Book

API_LIST_URL = "https://gutendex.com/books/?limit=100"

MAX_BOOKS = 100

def get_text_plain_link(formats: dict) -> str | None:
    for mime_type, url in formats.items():
        if mime_type.startswith("text/plain"):
            return url
    return None

async def load_books_metadata():
    async with AsyncSessionLocal() as session:

        result = await session.execute(select(Book.title))
        existing_titles = set(r[0] for r in result.all())

    async with httpx.AsyncClient() as client:
        url = API_LIST_URL
        valid_books = []

        while url and len(valid_books) < MAX_BOOKS:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            for book_data in data["results"]:
                if len(valid_books) >= MAX_BOOKS:
                    break

                title = book_data["title"]
                if title in existing_titles:
                    continue

                txt_link = get_text_plain_link(book_data.get("formats", {}))
                if not txt_link:
                    continue

                book = Book(
                    title=title,
                    author=book_data["authors"][0].get("name") if book_data["authors"] else "Unknown",
                    language=book_data["languages"][0] if book_data["languages"] else "en",
                    downloads=book_data["download_count"],
                    link=txt_link,
                    file_name=None,
                    embedding=None
                )
                valid_books.append(book)
                existing_titles.add(title) 

            url = data.get("next")

    async with AsyncSessionLocal() as session:
        session.add_all(valid_books)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(load_books_metadata())
