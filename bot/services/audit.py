import json
from typing import Any, Dict, Optional

from bot.db.models import AuditLog


class AuditLogService:
    """Persist admin and system activity records for compliance and auditing."""

    @staticmethod
    def record_event(
        session,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Any,
        user_telegram_id: Optional[int] = None,
        admin_telegram_id: Optional[int] = None,
        action: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        payload = details.copy() if isinstance(details, dict) else {"value": details}
        log_entry = AuditLog(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else None,
            user_telegram_id=user_telegram_id,
            admin_telegram_id=admin_telegram_id,
            action=action,
            details=json.dumps(payload, ensure_ascii=False),
        )
        session.add(log_entry)
        session.commit()
        return log_entry
