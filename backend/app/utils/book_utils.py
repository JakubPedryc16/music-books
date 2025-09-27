TEXT_DIR = "data/books/files/"
import aiofiles
import os

async def load_book_page(book_id: int, page: int, lines_per_page: int = 50):
    os.makedirs(TEXT_DIR, exist_ok=True)

    filename = f"{book_id}.txt"
    file_path = os.path.join(TEXT_DIR, filename)

    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        lines = await f.readlines()

    start_idx = (page - 1) * lines_per_page
    end_idx = page * lines_per_page

    page_lines = lines[start_idx:end_idx]
    return "".join(page_lines)
