from __future__ import annotations

from typing import Any, Dict, List

ROLE_CHAIN = [
    "developer_partner",
    "dealer",
    "vendor",
    "customer",
    "courier",
]


class MarketplacePolicy:
    """Real marketplace role and access policy aligned with the XalqUchun TZ model."""

    @staticmethod
    def validate_customer_access(user: Any) -> Dict[str, Any]:
        errors: List[str] = []

        if user is None:
            return {"allowed": False, "errors": ["user_missing"]}

        role = str(getattr(user, "role", "guest") or "guest").lower()
        if role != "customer":
            errors.append("role_invalid")

        if not getattr(user, "full_name", None) or not str(user.full_name).strip():
            errors.append("full_name_missing")
        if not getattr(user, "phone_number", None) or not str(user.phone_number).strip():
            errors.append("phone_missing")
        if not getattr(user, "is_phone_verified", False):
            errors.append("phone_not_verified")
        if not getattr(user, "is_kyc_verified", False):
            errors.append("kyc_not_verified")
        if not getattr(user, "address", None) or not str(user.address).strip():
            errors.append("address_missing")
        if not getattr(user, "passport_number", None) or not str(user.passport_number).strip():
            errors.append("passport_missing")

        return {"allowed": not errors, "errors": errors}


class MarketplaceRoleService:
    """Role flow enforcement for the chain: Developer Partner -> Dealer -> Vendor -> Customer -> Courier."""

    @staticmethod
    def ensure_chain(role: str) -> bool:
        return role.lower() in ROLE_CHAIN
