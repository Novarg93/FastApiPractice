from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# асинхронный движок
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,               # вывод SQL в логи, для отладки
    future=True
)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
