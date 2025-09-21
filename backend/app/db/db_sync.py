from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import DATABASE_URL

import os
os.makedirs("data/database", exist_ok=True)
os.makedirs("data/music", exist_ok=True)
os.makedirs("data/tags", exist_ok=True)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)