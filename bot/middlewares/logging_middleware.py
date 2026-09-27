# bot/middlewares/logging_middleware.py
"""
Logging middleware
Barcha eventlarni log qilish
"""
import logging
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """
    Barcha eventlarni log qilish va performance monitoring
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Boshlang'ich vaqt
        start_time = time.time()
        
        # Event haqida ma'lumot
        event_info = self.get_event_info(event)
        
        # Log
        logger.info(f"📥 Incoming: {event_info}")
        
        try:
            # Handler'ni chaqirish
            result = await handler(event, data)
            
            # Execution time
            execution_time = time.time() - start_time
            
            logger.info(
                f"✅ Processed: {event_info} "
                f"[{execution_time:.3f}s]"
            )
            
            return result
            
        except Exception as e:
            # Execution time
            execution_time = time.time() - start_time
            
            logger.error(
                f"❌ Error: {event_info} "
                f"[{execution_time:.3f}s] - {e}"
            )
            
            raise
    
    def get_event_info(self, event: TelegramObject) -> str:
        """Event haqida ma'lumot"""
        if isinstance(event, Message):
            user = event.from_user
            user_info = f"@{user.username or 'NoUsername'}:{user.id}"
            
            if event.text:
                content = f"text='{event.text[:50]}'"
            elif event.photo:
                content = "photo"
            elif event.document:
                content = "document"
            elif event.voice:
                content = "voice"
            elif event.video:
                content = "video"
            else:
                content = "unknown"
            
            return f"Message from {user_info} ({content})"
            
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            user_info = f"@{user.username or 'NoUsername'}:{user.id}"
            data = event.data or "no_data"
            
            return f"Callback from {user_info} (data='{data[:50]}')"
            
        else:
            return f"Unknown event: {type(event).__name__}"
