# bot/middlewares/auth.py
"""
Authentication middleware
Foydalanuvchilarni avtomatik ro'yxatdan o'tkazish
"""
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.database import get_session
from bot.db.models import User

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """
    Foydalanuvchilarni avtomatik ro'yxatdan o'tkazish
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # User olish
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        
        if not user:
            return await handler(event, data)
        
        # Database session olish
        async with get_session() as session:
            # Foydalanuvchini tekshirish/yaratish
            db_user = await self.get_or_create_user(session, user)
            
            # Data ga qo'shish
            data["db_user"] = db_user
            data["session"] = session
        
        # Handler'ni chaqirish
        return await handler(event, data)
    
    async def get_or_create_user(
        self,
        session: AsyncSession,
        tg_user
    ) -> User:
        """
        Foydalanuvchini database'dan olish yoki yaratish
        
        Args:
            session: Database session
            tg_user: Telegram user object
        
        Returns:
            User model instance
        """
        from sqlalchemy import select
        
        # Database'dan qidirish
        result = await session.execute(
            select(User).where(User.telegram_id == tg_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Mavjud foydalanuvchi - ma'lumotlarni yangilash
            if user.username != tg_user.username:
                user.username = tg_user.username
                logger.info(f"Username yangilandi: {tg_user.id}")
            
            if user.full_name != tg_user.full_name:
                user.full_name = tg_user.full_name
                logger.info(f"Full name yangilandi: {tg_user.id}")
            
            await session.commit()
            
        else:
            # Yangi foydalanuvchi - yaratish
            user = User(
                telegram_id=tg_user.id,
                username=tg_user.username,
                full_name=tg_user.full_name,
                role="guest"
            )
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            logger.info(
                f"Yangi foydalanuvchi: {tg_user.id} "
                f"(@{tg_user.username or 'NoUsername'})"
            )
        
        return user
