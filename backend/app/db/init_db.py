from app.db.db_async import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn_sync: None)