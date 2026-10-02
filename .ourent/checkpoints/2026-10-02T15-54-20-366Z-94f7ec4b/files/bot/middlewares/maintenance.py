# bot/middlewares/maintenance.py
"""
Maintenance (texnik xizmat) middleware
"""
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

logger = logging.getLogger(__name__)

# Global flag - texnik xizmat rejimi
MAINTENANCE_MODE = False


class MaintenanceMiddleware(BaseMiddleware):
    """
    Texnik xizmat rejimida foydalanuvchilarga xabar ko'rsatish
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Agar texnik xizmat rejimi yoqilgan bo'lsa
        if MAINTENANCE_MODE:
            user_id = None
            
            if isinstance(event, Message):
                user_id = event.from_user.id
            elif isinstance(event, CallbackQuery):
                user_id = event.from_user.id
            
            # Adminlar uchun ruxsat
            from bot.data import ALL_OWNER_IDS
            if user_id and user_id in ALL_OWNER_IDS:
                return await handler(event, data)
            
            # Oddiy foydalanuvchilarga xabar
            message = "🛠 Texnik ishlar olib borilmoqda. Iltimos, keyinroq urinib ko'ring."
            
            if isinstance(event, Message):
                await event.answer(message)
            elif isinstance(event, CallbackQuery):
                await event.answer(message, show_alert=True)
            
            return None
        
        # Normal rejimda handler'ni chaqirish
        return await handler(event, data)