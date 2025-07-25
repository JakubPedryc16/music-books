from sqlalchemy import Column, Integer, LargeBinary, String
from src.db.database import Base
from sqlalchemy.orm import relationship
from src.models.associations import book_tag_association

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    language = Column(String, index=True)
    downloads = Column(Integer)
    link = Column(String)
    file_name = Column(String)
    embedding = Column(LargeBinary)


    tags = relationship(
        "Tag",
        secondary=book_tag_association,
        back_populates="books"
    )