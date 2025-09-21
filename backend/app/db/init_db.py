from app.db.db_async import engine

async def init_db():
    async with engine.begin() as conn:
        pass  
