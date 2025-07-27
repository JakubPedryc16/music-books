from sqlalchemy import JSON, Column, ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import relationship
from src.db.database import Base

class BookFragment(Base):
    __tablename__ = "book_fragments"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    fragment_index = Column(Integer)
    embedding = Column(LargeBinary)
    tag_embedding = Column(JSON, nullable=True)

    book = relationship("Book", back_populates="fragments")