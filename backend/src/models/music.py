
from sqlalchemy import Base, Column, Integer, LargeBinary, String
from sqlalchemy.orm import relationship
from src.models.associations import music_tag_association

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    embedding = Column(LargeBinary)

    tags = relationship(
        "Tag",
        secondary=music_tag_association,
        back_populates="music"
    )
    