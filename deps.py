from collections.abc import AsyncGenerator
from database import sessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, engine

async def create_db_and_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionLocal() as session:
        yield session