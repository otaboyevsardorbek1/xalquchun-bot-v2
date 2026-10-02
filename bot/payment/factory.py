from typing import Dict, Type

from bot.payment.base import BasePaymentAdapter
from bot.payment.click import ClickPayment
from bot.payment.payme import PaymePayment


class PaymentAdapterFactory:
    """Build provider adapters for live payment flows."""

    _registry: Dict[str, Type[BasePaymentAdapter]] = {
        "payme": PaymePayment,
        "click": ClickPayment,
    }

    @classmethod
    def create(cls, provider: str) -> BasePaymentAdapter:
        key = (provider or "").strip().lower()
        adapter_cls = cls._registry.get(key)
        if adapter_cls is None:
            raise ValueError(f"Unsupported payment provider: {provider}")
        return adapter_cls()
