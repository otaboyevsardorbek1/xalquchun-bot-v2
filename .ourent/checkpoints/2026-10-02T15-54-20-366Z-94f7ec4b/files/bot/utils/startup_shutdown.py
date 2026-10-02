# bot/utils/startup_shutdown.py
"""
Bot ishga tushish va to'xtash vaqtida adminlarga xabar yuborish
"""
import time
import logging
from aiogram import Bot

logger = logging.getLogger(__name__)


async def on_startup_notify(bot: Bot):
    """Bot ishga tushganda adminlarga xabar"""
    from bot.data import ALL_OWNER_IDS
    
    date_now = time.strftime("%Y-%m-%d")
    time_now = time.strftime("%H:%M:%S")
    
    for admin_id in ALL_OWNER_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"✅ *Bot ishga tushdi!*\n📅 {date_now}\n⏰ {time_now}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Admin {admin_id} ga xabar yuborishda xato: {e}")


async def on_shutdown_notify(bot: Bot):
    """Bot to'xtaganda adminlarga xabar"""
    from bot.data import ALL_OWNER_IDS
    
    date_now = time.strftime("%Y-%m-%d")
    time_now = time.strftime("%H:%M:%S")
    
    for admin_id in ALL_OWNER_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"❌ *Bot to'xtadi!*\n📅 {date_now}\n⏰ {time_now}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Admin {admin_id} ga xabar yuborishda xato: {e}")