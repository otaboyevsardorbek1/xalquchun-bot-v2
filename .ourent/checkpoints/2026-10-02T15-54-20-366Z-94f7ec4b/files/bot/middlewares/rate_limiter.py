# bot/middlewares/rate_limiter.py
"""
Rate limiting middleware
Spamdan himoya qilish
"""
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.config import bot_settings
from bot.services.cache import rate_limiter

logger = logging.getLogger(__name__)


class RateLimiterMiddleware(BaseMiddleware):
    """
    Rate limiting - foydalanuvchilar chastotasini cheklash
    """
    
    def __init__(
        self,
        limit: int = None,
        period: int = 60
    ):
        """
        Args:
            limit: Maksimal so'rovlar soni (default: from settings)
            period: Vaqt oralig'i sekundlarda (default: 60)
        """
        self.limit = limit or bot_settings.max_requests_per_minute
        self.period = period
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Rate limiting o'chirilgan bo'lsa
        if not bot_settings.rate_limit_enabled:
            return await handler(event, data)
        
        # User ID olish
        user_id = None
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
        
        if not user_id:
            return await handler(event, data)
        
        # Adminlar uchun rate limit yo'q
        if user_id in bot_settings.all_admin_ids:
            return await handler(event, data)
        
        # Rate limit tekshirish
        key = f"user:{user_id}"
        is_allowed = await rate_limiter.is_allowed(
            key=key,
            limit=self.limit,
            period=self.period
        )
        
        if not is_allowed:
            logger.warning(f"Rate limit: user {user_id}")
            
            # Foydalanuvchiga xabar
            message = (
                "⚠️ Juda ko'p so'rov!\n\n"
                f"Iltimos, {self.period} soniya kutib turing."
            )
            
            if isinstance(event, Message):
                await event.answer(message)
            elif isinstance(event, CallbackQuery):
                await event.answer(message, show_alert=True)
            
            return None
        
        # Handler'ni chaqirish
        return await handler(event, data)
