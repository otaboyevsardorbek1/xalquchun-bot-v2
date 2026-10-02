"""Monitoring and health-check utilities for deployment."""

import logging
from typing import Any, Dict

from bot.config import bot_settings

logger = logging.getLogger(__name__)


def build_health_status() -> Dict[str, Any]:
    """Return a deployment-safe health payload for probes."""
    status = {
        "status": "ok",
        "service": "telegram-bot",
        "bot_token_configured": bool(bot_settings.bot_token),
        "owner_configured": bool(bot_settings.owner_id),
        "maintenance_mode": bool(bot_settings.maintenance_mode),
        "cache_enabled": bool(bot_settings.cache_enabled),
        "webhook_configured": bool(bot_settings.webhook_url),
    }

    if not status["bot_token_configured"] or not status["owner_configured"]:
        status["status"] = "degraded"
        logger.warning("Health check detected missing runtime configuration.")

    return status
