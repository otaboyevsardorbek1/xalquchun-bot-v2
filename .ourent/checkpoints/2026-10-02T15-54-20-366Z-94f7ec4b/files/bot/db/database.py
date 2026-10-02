# bot/db/database.py
"""
Database connection va session management
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, QueuePool

from bot.config import bot_settings

logger = logging.getLogger(__name__)

# Global engine va session factory
engine: AsyncEngine = None
async_session_factory: async_sessionmaker = None


def create_engine() -> AsyncEngine:
    """Async database engine yaratish"""
    engine_kwargs = {
        "echo": False,
        "future": True,
        "pool_pre_ping": True,
    }
    
    if bot_settings.database_url.startswith("sqlite"):
        engine_kwargs["poolclass"] = NullPool
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        engine_kwargs["poolclass"] = QueuePool
        engine_kwargs["pool_size"] = 20
        engine_kwargs["max_overflow"] = 10
    
    return create_async_engine(bot_settings.database_url, **engine_kwargs)


async def init_db():
    """Database'ni ishga tushirish"""
    global engine, async_session_factory
    
    engine = create_engine()
    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    from bot.db.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database tayyor")


async def close_db():
    """Database yopish"""
    if engine:
        await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Session olish"""
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
