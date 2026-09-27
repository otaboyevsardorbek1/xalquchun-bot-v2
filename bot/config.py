# bot/config.py
"""
Yaxshilangan konfiguratsiya tizimi
"""
import os
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Muhit o'zgaruvchilarini yuklash
load_dotenv()

logger = logging.getLogger(__name__)


class BotSettings:
    """Bot asosiy sozlamalari"""
    
    def __init__(self):
        # Bot token
        self.bot_token: str = os.getenv("BOT_TOKEN", "")
        
        # Adminlar
        self.owner_id: int = int(os.getenv("OWNER_ID", "0"))
        self.admin_ids: List[int] = self._parse_admin_ids(
            os.getenv("ADMIN_IDS", "")
        )
        
        # Database
        self.database_url: str = os.getenv(
            "DATABASE_URL", 
            "sqlite+aiosqlite:///./database.sqlite3"
        )
        self.redis_url: Optional[str] = os.getenv("REDIS_URL") or None
        
        # Webhook
        self.webhook_host: Optional[str] = os.getenv("WEBHOOK_HOST") or None
        self.webhook_path: str = os.getenv("WEBHOOK_PATH", "/webhook")
        self.web_server_host: str = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
        self.web_server_port: int = int(os.getenv("WEB_SERVER_PORT", "8080"))
        self.healthcheck_enabled: bool = os.getenv("HEALTHCHECK_ENABLED", "true").lower() == "true"
        self.healthcheck_port: int = int(os.getenv("HEALTHCHECK_PORT", "8081"))
        
        # Fly.io
        self.fly_app_name: Optional[str] = os.getenv("FLY_APP_NAME") or None
        self.is_fly_io: bool = bool(self.fly_app_name)
        
        # Loglar
        self.log_file: Optional[str] = os.getenv("LOG_FILE", "bot.log")
        self.max_log_size_mb: int = int(os.getenv("MAX_LOG_SIZE_MB", "20"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Cache
        self.cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
        
        # Xavfsizlik
        self.jwt_secret_key: str = os.getenv(
            "JWT_SECRET_KEY", 
            "change-this-secret-key"
        )
        self.session_timeout: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
        self.max_login_attempts: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        
        # Maintenance
        self.maintenance_mode: bool = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
        self.maintenance_message: str = os.getenv(
            "MAINTENANCE_MESSAGE", 
            "Texnik ishlar olib borilmoqda..."
        )
        
        # Rate limiting
        self.rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
        self.max_requests_per_minute: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))
        
        # File storage
        self.max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
        self.backup_dir: str = os.getenv("BACKUP_DIR", "backups")
        
        # Kanal/Guruh
        channel_id_str = os.getenv("CHANNEL_ID")
        self.channel_id: Optional[int] = int(channel_id_str) if channel_id_str else None
        
        support_group_id_str = os.getenv("SUPPORT_GROUP_ID")
        self.support_group_id: Optional[int] = (
            int(support_group_id_str) if support_group_id_str else None
        )
    
    @staticmethod
    def _parse_admin_ids(admin_ids_str: str) -> List[int]:
        """Admin ID larni parse qilish"""
        if not admin_ids_str or not admin_ids_str.strip():
            return []
        
        admin_ids_str = admin_ids_str.strip()
        
        # JSON formatida bo'lsa: [123, 456]
        if admin_ids_str.startswith("["):
            try:
                return json.loads(admin_ids_str)
            except json.JSONDecodeError:
                pass
        
        # Vergul bilan ajratilgan: 123,456
        try:
            return [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
        except ValueError:
            return []
    
    @property
    def webhook_url(self) -> Optional[str]:
        """Webhook URL ni olish va normalizatsiya qilish."""
        if not self.webhook_host:
            return None

        host = self.webhook_host.strip().rstrip("/")
        if not host.startswith(("http://", "https://")):
            host = f"https://{host}"

        return f"{host}{self.webhook_path}"
    
    @property
    def all_admin_ids(self) -> List[int]:
        """Barcha adminlar (owner + adminlar)"""
        return list(set([self.owner_id] + self.admin_ids))


class PaymentSettings:
    """To'lov tizimi sozlamalari"""
    
    def __init__(self):
        # Click.uz
        self.click_merchant_id: Optional[str] = os.getenv("CLICK_MERCHANT_ID") or None
        self.click_service_id: Optional[str] = os.getenv("CLICK_SERVICE_ID") or None
        self.click_secret_key: Optional[str] = os.getenv("CLICK_SECRET_KEY") or None
        self.click_merchant_user_id: Optional[str] = os.getenv("CLICK_MERCHANT_USER_ID") or None
        
        # Payme
        self.payme_merchant_id: Optional[str] = os.getenv("PAYME_MERCHANT_ID") or None
        self.payme_secret_key: Optional[str] = os.getenv("PAYME_SECRET_KEY") or None
        self.payme_test_mode: bool = os.getenv("PAYME_TEST_MODE", "true").lower() == "true"
    
    @property
    def is_click_enabled(self) -> bool:
        """Click.uz yoqilganmi?"""
        return all([
            self.click_merchant_id,
            self.click_service_id,
            self.click_secret_key
        ])
    
    @property
    def is_payme_enabled(self) -> bool:
        """Payme yoqilganmi?"""
        return all([self.payme_merchant_id, self.payme_secret_key])


class SMSSettings:
    """SMS provider sozlamalari"""
    
    def __init__(self):
        # Eskiz.uz
        self.eskiz_email: Optional[str] = os.getenv("ESKIZ_EMAIL") or None
        self.eskiz_password: Optional[str] = os.getenv("ESKIZ_PASSWORD") or None
        
        # PlayMobile
        self.playmobile_login: Optional[str] = os.getenv("PLAYMOBILE_LOGIN") or None
        self.playmobile_password: Optional[str] = os.getenv("PLAYMOBILE_PASSWORD") or None
    
    @property
    def is_eskiz_enabled(self) -> bool:
        """Eskiz.uz yoqilganmi?"""
        return all([self.eskiz_email, self.eskiz_password])
    
    @property
    def is_playmobile_enabled(self) -> bool:
        """PlayMobile yoqilganmi?"""
        return all([self.playmobile_login, self.playmobile_password])


class ReferralSettings:
    """Referral tizimi sozlamalari"""
    
    def __init__(self):
        self.max_tree_depth: int = int(os.getenv("MAX_TREE_DEPTH", "15"))
        self.level_1_reward: float = float(os.getenv("LEVEL_1_REWARD", "100.0"))
        self.level_2_reward: float = float(os.getenv("LEVEL_2_REWARD", "50.0"))
        self.level_3_reward: float = float(os.getenv("LEVEL_3_REWARD", "25.0"))
        self.level_4_reward: float = float(os.getenv("LEVEL_4_REWARD", "10.0"))
        self.level_5_reward: float = float(os.getenv("LEVEL_5_REWARD", "5.0"))
    
    @property
    def level_rewards(self) -> Dict[int, float]:
        """Darajalar bo'yicha mukofotlar"""
        return {
            1: self.level_1_reward,
            2: self.level_2_reward,
            3: self.level_3_reward,
            4: self.level_4_reward,
            5: self.level_5_reward,
        }


class APISettings:
    """Tashqi API sozlamalari"""
    
    def __init__(self):
        # AI
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY") or None
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY") or None
        
        # Maps
        self.google_maps_api_key: Optional[str] = os.getenv("GOOGLE_MAPS_API_KEY") or None
        
        # Monitoring
        self.sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN") or None


# ==================== GLOBAL SETTINGS ====================

bot_settings = BotSettings()
payment_settings = PaymentSettings()
sms_settings = SMSSettings()
referral_settings = ReferralSettings()
api_settings = APISettings()


def validate_runtime_settings(settings: Optional[BotSettings] = None) -> None:
    """Foydalanishdan oldin kerakli runtime sozlamalarni tekshirish."""
    settings = settings or bot_settings
    missing: List[str] = []

    if not settings.bot_token or not settings.bot_token.strip():
        missing.append("BOT_TOKEN")

    if not settings.owner_id:
        missing.append("OWNER_ID")

    if missing:
        raise RuntimeError(
            "Missing required runtime configuration: " + ", ".join(missing)
        )


# ==================== LOGGING KONFIGURATSIYASI ====================

def setup_logging():
    """Logging tizimini sozlash"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler()]
    
    if bot_settings.log_file and not bot_settings.is_fly_io:
        handlers.append(
            logging.FileHandler(bot_settings.log_file, encoding="utf-8")
        )
    
    logging.basicConfig(
        level=getattr(logging, bot_settings.log_level),
        format=log_format,
        handlers=handlers
    )
    
    # Aiogram loglarni cheklash
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)


# ==================== PAPKALARNI YARATISH ====================

def create_directories():
    """Kerakli papkalarni yaratish"""
    directories = [
        bot_settings.upload_dir,
        bot_settings.backup_dir,
        "logs",
        "temp",
    ]
    
    if bot_settings.is_fly_io:
        directories.append("/data")
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Papka yaratildi: {directory}")


# ==================== KONFIGURATSIYANI CHIQARISH ====================

def print_config():
    """Konfiguratsiyani ko'rsatish"""
    logger.info("=" * 60)
    logger.info("🤖 BOT KONFIGURATSIYASI")
    logger.info("=" * 60)
    logger.info(f"  • Bot token: {'✅' if bot_settings.bot_token else '❌'}")
    logger.info(f"  • Owner ID: {bot_settings.owner_id}")
    logger.info(f"  • Admin IDs: {bot_settings.admin_ids}")
    logger.info(f"  • Database: {bot_settings.database_url}")
    logger.info(f"  • Redis: {'✅' if bot_settings.redis_url else '❌'}")
    logger.info(f"  • Webhook: {'✅' if bot_settings.webhook_url else '❌'}")
    logger.info(f"  • Fly.io: {'✅' if bot_settings.is_fly_io else '❌'}")
    logger.info(f"  • Cache: {'✅' if bot_settings.cache_enabled else '❌'}")
    logger.info(f"  • Maintenance: {'✅' if bot_settings.maintenance_mode else '❌'}")
    logger.info("=" * 60)
    logger.info("💳 TO'LOV TIZIMLARI")
    logger.info("=" * 60)
    logger.info(f"  • Click.uz: {'✅' if payment_settings.is_click_enabled else '❌'}")
    logger.info(f"  • Payme: {'✅' if payment_settings.is_payme_enabled else '❌'}")
    logger.info("=" * 60)
    logger.info("📱 SMS PROVIDERLAR")
    logger.info("=" * 60)
    logger.info(f"  • Eskiz.uz: {'✅' if sms_settings.is_eskiz_enabled else '❌'}")
    logger.info(f"  • PlayMobile: {'✅' if sms_settings.is_playmobile_enabled else '❌'}")
    logger.info("=" * 60)


# Avtomatik sozlash
setup_logging()
create_directories()
validate_runtime_settings()
print_config()