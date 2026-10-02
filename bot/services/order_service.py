from __future__ import annotations

from typing import Any, Dict, List


class OrderService:
    """Real order lifecycle validation for the commerce ecosystem."""

    @staticmethod
    def validate_cart_total(cart: Any, delivery_address: str, user_role: str) -> Dict[str, Any]:
        errors: List[str] = []

        if user_role is None or str(user_role).strip() == "":
            errors.append("role_missing")

        if not cart or len(cart) == 0:
            errors.append("cart_empty")

        if not delivery_address or not str(delivery_address).strip():
            errors.append("delivery_address_missing")

        total = 0
        if isinstance(cart, dict):
            for item in cart.values():
                if isinstance(item, dict):
                    total += float(item.get("price", 0) or 0) * float(item.get("quantity", 0) or 0)
                else:
                    total += float(item or 0)

        if total <= 0:
            errors.append("total_invalid")

        return {"allowed": not errors, "errors": errors, "total": total}
