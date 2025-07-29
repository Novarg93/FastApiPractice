from database.session import engine, Base

async def init_db():
    """
    Создаёт все таблицы, описанные в Base.metadata
    """
    async with engine.begin() as conn:
        # если нужно — можно добавить drop_all()
        await conn.run_sync(Base.metadata.create_all)

