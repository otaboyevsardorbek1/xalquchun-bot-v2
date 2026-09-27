# bot/middlewares/error_handler.py
"""
Error handling middleware
Xatolarni ushlab adminlarga xabar berish
"""
import logging
import traceback
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram import Bot

from bot.config import bot_settings

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseMiddleware):
    """
    Xatolarni ushlab qolish va adminlarga xabar berish
    """
    
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            # Handlerni chaqirish
            return await handler(event, data)
            
        except Exception as e:
            # Xatoni log qilish
            logger.error(f"Handler xatosi: {e}", exc_info=True)
            
            # Foydalanuvchiga xabar
            await self.notify_user(event, e)
            
            # Adminlarga xabar
            await self.notify_admins(event, e)
            
            # Xatoni qayta raise qilmaslik (botni to'xtatmaslik)
            return None
    
    async def notify_user(self, event: TelegramObject, error: Exception):
        """Foydalanuvchiga xabar yuborish"""
        try:
            message_text = (
                "❌ Xatolik yuz berdi!\n\n"
                "Iltimos, keyinroq qayta urinib ko'ring yoki "
                "administratorga murojaat qiling.\n\n"
                "📞 Aloqa: /info"
            )
            
            if isinstance(event, Message):
                await event.answer(message_text)
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "❌ Xatolik yuz berdi! Keyinroq urinib ko'ring.",
                    show_alert=True
                )
                
        except Exception as e:
            logger.error(f"Foydalanuvchiga xabar yuborish xatosi: {e}")
    
    async def notify_admins(self, event: TelegramObject, error: Exception):
        """Adminlarga xabar yuborish"""
        try:
            # User info
            user_info = "Noma'lum"
            event_type = "Unknown"
            
            if isinstance(event, Message):
                user = event.from_user
                user_info = f"@{user.username or 'NoUsername'} (ID: {user.id})"
                event_type = "Message"
                text = event.text or event.caption or "No text"
            elif isinstance(event, CallbackQuery):
                user = event.from_user
                user_info = f"@{user.username or 'NoUsername'} (ID: {user.id})"
                event_type = "CallbackQuery"
                text = event.data or "No data"
            else:
                text = "Unknown event"
            
            # Error info
            error_text = str(error)
            error_type = type(error).__name__
            
            # Traceback
            tb = traceback.format_exc()
            
            # Xabar matni
            message = (
                f"🚨 <b>BOT XATOSI!</b>\n\n"
                f"<b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"<b>Foydalanuvchi:</b> {user_info}\n"
                f"<b>Event:</b> {event_type}\n"
                f"<b>Text:</b> <code>{text[:100]}</code>\n\n"
                f"<b>Xato turi:</b> {error_type}\n"
                f"<b>Xato:</b> <code>{error_text[:200]}</code>\n\n"
                f"<b>Traceback:</b>\n<pre>{tb[:1000]}</pre>"
            )
            
            # Adminlarga yuborish
            for admin_id in bot_settings.all_admin_ids:
                try:
                    await self.bot.send_message(admin_id, message)
                except Exception as e:
                    logger.error(f"Admin {admin_id} ga xabar yuborish xatosi: {e}")
                    
        except Exception as e:
            logger.error(f"Adminlarga xabar yuborish xatosi: {e}")
