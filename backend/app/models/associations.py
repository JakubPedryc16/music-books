
from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.database import Base


book_tag_association = Table(
    "book_tag_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"),  primary_key=True)
)

music_tag_association = Table(
    "music_tag_association",
    Base.metadata,
    Column("music_id", Integer, ForeignKey("music.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"),  primary_key=True)
)