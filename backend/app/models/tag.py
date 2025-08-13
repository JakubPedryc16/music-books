
from sqlalchemy import Column, Integer, String
from app.db.database import Base

from sqlalchemy.orm import relationship
from app.models.associations import music_tag_association, book_tag_association


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, index=True, unique=True)

    music = relationship(
        "Music",
        secondary=music_tag_association,
        back_populates="tags"
    )

    books = relationship(
        "Book",
        secondary=book_tag_association,
        back_populates="tags"
    )