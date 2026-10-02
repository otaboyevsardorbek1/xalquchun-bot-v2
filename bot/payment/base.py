from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePaymentAdapter(ABC):
    """Base adapter for real gateway integrations used in checkout."""

    @abstractmethod
    def create_payment_url(self, amount: float, order_id: str, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def complete_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
