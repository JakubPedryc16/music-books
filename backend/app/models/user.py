import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True, nullable=False)
    display_name = Column(String)
    email = Column(String, nullable=True)
    access_token = Column(String, nullable=False) 
    refresh_token = Column(String, nullable=False) 
    token_expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))