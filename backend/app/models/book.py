from sqlalchemy import JSON, Column, Integer, LargeBinary, String
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    language = Column(String, index=True)
    downloads = Column(Integer)
    link = Column(String)
    file_name = Column(String)
    