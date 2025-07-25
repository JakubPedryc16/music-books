from sqlalchemy import Column, Integer, LargeBinary, String, Text, Float
from sqlalchemy.orm import relationship
from src.models.associations import music_tag_association
from src.db.database import Base

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    lyrics = Column(Text)
    embedding = Column(LargeBinary)

    spotify_id = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)

    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    liveness = Column(Float, nullable=True)
    speechiness = Column(Float, nullable=True)

    tags = relationship(
        "Tag",
        secondary=music_tag_association,
        back_populates="music"
    )
