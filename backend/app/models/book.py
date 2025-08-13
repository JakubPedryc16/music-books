from sqlalchemy import JSON, Column, Integer, LargeBinary, String
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.associations import book_tag_association

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    language = Column(String, index=True)
    downloads = Column(Integer)
    link = Column(String)
    file_name = Column(String)
    
    embedding = Column(LargeBinary, nullable=True)
    embedding_tags = Column(JSON, nullable=True)


    fragments = relationship("BookFragment", back_populates="book", cascade="all, delete-orphan")

    tags = relationship(
        "Tag",
        secondary=book_tag_association,
        back_populates="books"
    )