# main.py
import sys
import os
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Local imports
from bot.config import bot_settings, print_config
from bot.db.database import init_db, close_db
from bot.monitoring import build_health_status
from bot.services.cache import cache_service
from bot.services.sms import otp_cleanup_task

# Handlerlarni import qilish
from bot.handlers import (
    start,
    catalog,
    cart,
    checkout,
    admin,
    profile,
    referral,
    payment_handlers,
)

# Middlewarelarni import qilish
from bot.middlewares.error_handler import ErrorHandlerMiddleware
from bot.middlewares.logging_middleware import LoggingMiddleware
from bot.middlewares.rate_limiter import RateLimiterMiddleware
from bot.middlewares.maintenance import MaintenanceMiddleware
from bot.middlewares.auth import AuthMiddleware

# Utilitylar
from bot.utils.startup_shutdown import (
    on_startup_notify,
    on_shutdown_notify
)

# Logging sozlash
logger = logging.getLogger(__name__)


def register_health_routes(app: web.Application) -> None:
    """Health-check va readiness endpointlarini ro'yxatdan o'tkazish."""

    async def health_check(request):
        payload = build_health_status()
        status_code = 200 if payload.get("status") == "ok" else 503
        return web.json_response(payload, status=status_code)

    app.router.add_get("/health", health_check)
    app.router.add_get("/healthz", health_check)
    app.router.add_get("/readyz", health_check)


class BotApplication:
    """Bot application manager"""
    
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.webapp: Optional[web.Application] = None
        self._runners = []
        
    def setup_bot(self):
        """Bot va dispatcher'ni sozlash"""
        logger.info("🤖 Bot sozlanmoqda...")
        
        # Bot instance
        self.bot = Bot(
            token=bot_settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Dispatcher (FSM storage)
        storage = MemoryStorage()
        self.dp = Dispatcher(storage=storage)
        
        logger.info("✅ Bot sozlandi")
    
    def setup_middlewares(self):
        """Middlewarelarni ulash"""
        logger.info("⚙️ Middlewarelar sozlanmoqda...")
        
        # Message middlewares
        self.dp.message.middleware(LoggingMiddleware())
        self.dp.message.middleware(ErrorHandlerMiddleware(self.bot))
        self.dp.message.middleware(RateLimiterMiddleware())
        self.dp.message.middleware(MaintenanceMiddleware())
        self.dp.message.middleware(AuthMiddleware())
        
        # Callback middlewares
        self.dp.callback_query.middleware(LoggingMiddleware())
        self.dp.callback_query.middleware(ErrorHandlerMiddleware(self.bot))
        self.dp.callback_query.middleware(RateLimiterMiddleware())
        self.dp.callback_query.middleware(MaintenanceMiddleware())
        self.dp.callback_query.middleware(AuthMiddleware())
        
        logger.info("✅ Middlewarelar ulandi")
    
    def setup_routers(self):
        """Handlerlarni ulash"""
        logger.info("📡 Handlerlar sozlanmoqda...")
        
        # Routerlarni tartibi muhim!
        routers = [
            start.router,
            catalog.router,
            cart.router,
            checkout.router,
            payment_handlers.router,
            profile.router,
            referral.router,
            admin.router,
        ]
        
        for router in routers:
            self.dp.include_router(router)
        
        logger.info(f"✅ {len(routers)} ta handler ulandi")
    
    async def set_bot_commands(self):
        """Bot komandalarini o'rnatish"""
        logger.info("📋 Bot komandalari o'rnatilmoqda...")
        
        commands = [
            BotCommand(command="start", description="🚀 Botni ishga tushirish"),
            BotCommand(command="help", description="❓ Yordam"),
            BotCommand(command="catalog", description="🛍 Mahsulotlar katalogi"),
            BotCommand(command="cart", description="🛒 Savat"),
            BotCommand(command="profile", description="👤 Profil"),
            BotCommand(command="balance", description="💰 Balans"),
            BotCommand(command="referral", description="🎁 Referral dasturi"),
        ]
        
        # Admin komandalari
        if bot_settings.owner_id in bot_settings.all_admin_ids:
            commands.extend([
                BotCommand(command="admin", description="👑 Admin panel"),
                BotCommand(command="stats", description="📊 Statistika"),
                BotCommand(command="broadcast", description="📢 Xabar yuborish"),
            ])
        
        await self.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        
        logger.info(f"✅ {len(commands)} ta komanda o'rnatildi")
    
    async def on_startup(self):
        """Bot ishga tushganda"""
        logger.info("=" * 70)
        logger.info("🚀 BOT ISHGA TUSHMOQDA...")
        logger.info("=" * 70)
        
        try:
            # 1. Konfiguratsiyani ko'rsatish
            print_config()
            
            # 2. Database'ni ishga tushirish
            logger.info("1️⃣ Database ishga tushirilmoqda...")
            await init_db()
            logger.info("   ✅ Database tayyor")
            
            # 3. Cache'ni ishga tushirish
            if bot_settings.cache_enabled:
                logger.info("2️⃣ Cache ishga tushirilmoqda...")
                await cache_service.initialize()
                logger.info("   ✅ Cache tayyor")
            
            # 4. Bot komandalarini o'rnatish
            logger.info("3️⃣ Bot komandalari o'rnatilmoqda...")
            await self.set_bot_commands()
            logger.info("   ✅ Komandalar o'rnatildi")
            
            # 5. Background tasklar
            logger.info("4️⃣ Background tasklar ishga tushirilmoqda...")
            asyncio.create_task(otp_cleanup_task())
            logger.info("   ✅ Background tasklar ishga tushdi")
            
            # 6. Adminlarni xabardor qilish
            logger.info("5️⃣ Adminlar xabardor qilinmoqda...")
            await on_startup_notify(self.bot)
            logger.info("   ✅ Adminlar xabardor qilindi")
            
            # 7. Bot ma'lumotlari
            bot_info = await self.bot.get_me()
            logger.info("=" * 70)
            logger.info(f"🤖 Bot: @{bot_info.username}")
            logger.info(f"🆔 ID: {bot_info.id}")
            logger.info(f"👤 Owner: {bot_settings.owner_id}")
            logger.info(f"👥 Adminlar: {bot_settings.admin_ids}")
            logger.info(f"🌍 Muhit: {'Fly.io' if bot_settings.is_fly_io else 'Lokal'}")
            logger.info(f"🔧 Webhook: {'✅' if bot_settings.webhook_url else '❌'}")
            logger.info(f"💾 Cache: {'✅' if bot_settings.cache_enabled else '❌'}")
            logger.info(f"🔒 Maintenance: {'✅' if bot_settings.maintenance_mode else '❌'}")
            logger.info("=" * 70)
            logger.info("✅ BOT MUVAFFAQIYATLI ISHGA TUSHDI!")
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error("=" * 70)
            logger.error(f"❌ ISHGA TUSHISH XATOSI: {e}", exc_info=True)
            logger.error("=" * 70)
            raise
    
    async def on_shutdown(self):
        """Bot to'xtaganda"""
        logger.info("=" * 70)
        logger.info("🛑 BOT TO'XTATILMOQDA...")
        logger.info("=" * 70)
        
        try:
            if self._runners:
                logger.info("1️⃣ Health serverlar yopilmoqda...")
                for runner in self._runners:
                    await runner.cleanup()
                logger.info("   ✅ Health serverlar yopildi")

            # 2. Adminlarni xabardor qilish
            logger.info("2️⃣ Adminlar xabardor qilinmoqda...")
            await on_shutdown_notify(self.bot)
            logger.info("   ✅ Adminlar xabardor qilindi")
            
            # 3. Cache'ni yopish
            if bot_settings.cache_enabled:
                logger.info("3️⃣ Cache yopilmoqda...")
                await cache_service.shutdown()
                logger.info("   ✅ Cache yopildi")
            
            # 4. Database'ni yopish
            logger.info("4️⃣ Database yopilmoqda...")
            await close_db()
            logger.info("   ✅ Database yopildi")
            
            # 5. Bot sessionni yopish
            logger.info("5️⃣ Bot session yopilmoqda...")
            await self.bot.session.close()
            logger.info("   ✅ Bot session yopildi")
            
            logger.info("=" * 70)
            logger.info("✅ BOT MUVAFFAQIYATLI TO'XTATILDI!")
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error(f"❌ TO'XTATISH XATOSI: {e}", exc_info=True)
    
    async def start_health_server(self):
        """Polling rejimida health-check serverini ishga tushirish."""
        if not bot_settings.healthcheck_enabled:
            logger.info("🩺 Health-check o'chirilgan")
            return

        self.webapp = web.Application()
        register_health_routes(self.webapp)

        runner = web.AppRunner(self.webapp)
        await runner.setup()
        self._runners.append(runner)

        site = web.TCPSite(
            runner,
            host=bot_settings.web_server_host,
            port=bot_settings.healthcheck_port,
        )
        await site.start()

        logger.info(
            "🩺 Health-check serveri ishga tushdi: "
            f"http://{bot_settings.web_server_host}:{bot_settings.healthcheck_port}/healthz"
        )

    async def start_polling(self):
        """Polling rejimda ishga tushirish"""
        logger.info("🔄 Polling rejimi...")

        await self.start_health_server()

        # Startup
        await self.on_startup()
        
        try:
            # Polling
            await self.dp.start_polling(
                self.bot,
                allowed_updates=self.dp.resolve_used_update_types()
            )
        finally:
            # Shutdown
            await self.on_shutdown()
    
    async def start_webhook(self):
        """Webhook rejimda ishga tushirish"""
        logger.info("🌐 Webhook rejimi...")
        
        if not bot_settings.webhook_url:
            raise ValueError("WEBHOOK_URL sozlanmagan!")
        
        # Startup
        await self.on_startup()
        
        # Webhook o'rnatish
        await self.bot.set_webhook(
            url=bot_settings.webhook_url,
            drop_pending_updates=True
        )
        
        logger.info(f"✅ Webhook o'rnatildi: {bot_settings.webhook_url}")
        
        # Web server
        self.webapp = web.Application()
        register_health_routes(self.webapp)
        
        # Webhook handler
        webhook_handler = SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot
        )
        webhook_handler.register(self.webapp, path=bot_settings.webhook_path)
        
        # Health check endpoint
        async def health_check(request):
            return web.Response(text="OK")
        
        self.webapp.router.add_get("/health", health_check)
        
        # Cleanup
        setup_application(self.webapp, self.dp, bot=self.bot)
        
        # Serverni ishga tushirish
        runner = web.AppRunner(self.webapp)
        await runner.setup()
        self._runners.append(runner)
        
        site = web.TCPSite(
            runner,
            host=bot_settings.web_server_host,
            port=bot_settings.web_server_port
        )
        
        logger.info(
            f"🌐 Web server: {bot_settings.web_server_host}:{bot_settings.web_server_port}"
        )
        
        await site.start()
        
        # Cheksiz kutish
        try:
            await asyncio.Event().wait()
        finally:
            await self.on_shutdown()
    
    async def run(self):
        """Botni ishga tushirish"""
        # Bot va handlerlarni sozlash
        self.setup_bot()
        self.setup_middlewares()
        self.setup_routers()
        
        # Webhook yoki polling
        if bot_settings.webhook_url:
            await self.start_webhook()
        else:
            await self.start_polling()


def main():
    """Asosiy funksiya"""
    try:
        # Application yaratish
        app = BotApplication()
        
        # Ishga tushirish
        asyncio.run(app.run())
        
    except KeyboardInterrupt:
        logger.info("👋 Bot foydalanuvchi tomonidan to'xtatildi")
    except SystemExit:
        logger.info("👋 Bot tizim tomonidan to'xtatildi")
    except Exception as e:
        logger.error(f"💥 Kritik xato: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
