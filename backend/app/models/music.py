from sqlalchemy import JSON, Column, Integer, LargeBinary, String, Text, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    lyrics = Column(Text)

    spotify_id = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)

    embedding = Column(LargeBinary, nullable=True)
    embedding_tags = Column(JSON, nullable=True)
    embedding_emotions = Column(JSON, nullable=True)
    spotify_features = Column(JSON, nullable=True)