# bot/payment/payme.py
"""
Payme to'lov tizimi integratsiyasi
Merchant API v2.0
"""
import base64
import hashlib
import logging
import time
from typing import Optional, Dict, Any
from datetime import datetime
import aiohttp
from bot.config import payment_settings
from bot.payment.base import BasePaymentAdapter

logger = logging.getLogger(__name__)


class PaymeError(Exception):
    """Payme xatoligi"""
    
    # Payme error codes
    ERRORS = {
        -32504: "Недостаточно привилегий для выполнения метода",
        -31050: "Неверная сумма",
        -31051: "Неверный account",
        -31052: "Заказ не найден",
        -31053: "Невозможно выполнить операцию",
        -31054: "Заказ не активен",
        -31055: "Заказ уже завершён",
        -31099: "Заказ отменён",
    }
    
    def __init__(self, code: int, message: str = None, data: Any = None):
        self.code = code
        self.message = message or self.ERRORS.get(code, "Unknown error")
        self.data = data
        super().__init__(self.message)
    
    def to_dict(self):
        """Error ni dict ga aylantirish"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "data": self.data
            }
        }


class PaymePayment(BasePaymentAdapter):
    """Payme to'lov tizimi"""
    
    # Transaction states
    STATE_CREATED = 1
    STATE_COMPLETED = 2
    STATE_CANCELLED = -1
    STATE_CANCELLED_AFTER_COMPLETE = -2
    
    # Reasons
    REASON_RECEIVERS_NOT_FOUND = 1
    REASON_PROCESSING_EXECUTION_FAILED = 2
    REASON_EXECUTION_FAILED = 3
    REASON_CANCELLED_BY_TIMEOUT = 4
    REASON_FUND_RETURNED = 5
    REASON_UNKNOWN = 10
    
    def __init__(self):
        self.merchant_id = payment_settings.payme_merchant_id
        self.secret_key = payment_settings.payme_secret_key
        self.test_mode = payment_settings.payme_test_mode
        
        # API URLs
        if self.test_mode:
            self.api_url = "https://checkout.test.paycom.uz/api"
            self.checkout_url = "https://checkout.test.paycom.uz"
        else:
            self.api_url = "https://checkout.paycom.uz/api"
            self.checkout_url = "https://checkout.paycom.uz"
    
    def generate_pay_link(
        self,
        amount: float,
        order_id: str,
        return_url: str = None,
        description: str = None
    ) -> str:
        """
        To'lov havolasi yaratish
        
        Args:
            amount: To'lov summasi (tiyin)
            order_id: Buyurtma ID
            return_url: Qaytish URL
            description: Izoh
        
        Returns:
            To'lov havolasi
        """
        # Amount ni tiyin ga o'tkazish (100 so'm = 10000 tiyin)
        amount_in_tiyin = int(amount * 100)
        
        # Account parametrlari
        account = {
            "order_id": order_id
        }
        
        # Base64 encode
        account_b64 = base64.b64encode(
            f"order_id={order_id}".encode()
        ).decode()
        
        # URL yaratish
        url = f"{self.checkout_url}/{self.merchant_id}"
        url += f"?amount={amount_in_tiyin}"
        url += f"&account.order_id={order_id}"
        
        if return_url:
            url += f"&callback={return_url}"
        
        logger.info(f"Payme to'lov havolasi: order_id={order_id}, amount={amount}")
        
        return url
    
    def check_authorization(self, headers: Dict[str, str]) -> bool:
        """
        Authorization headerini tekshirish
        
        Args:
            headers: Request headers
        
        Returns:
            True agar autentifikatsiya to'g'ri bo'lsa
        """
        try:
            auth_header = headers.get("Authorization", "")
            
            if not auth_header.startswith("Basic "):
                logger.error("Payme auth header noto'g'ri")
                return False
            
            # Basic auth decode
            auth_b64 = auth_header.replace("Basic ", "")
            auth_decoded = base64.b64decode(auth_b64).decode()
            
            # Format: "Paycom:{secret_key}"
            if not auth_decoded.startswith("Paycom:"):
                logger.error("Payme auth format xato")
                return False
            
            provided_key = auth_decoded.split(":", 1)[1]
            
            if provided_key != self.secret_key:
                logger.error("Payme secret key xato")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Payme auth tekshirish xatosi: {e}")
            return False
    
    async def check_perform_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        CheckPerformTransaction - to'lovni amalga oshirish mumkinligini tekshirish
        
        Args:
            params: {
                "amount": int,  # tiyin
                "account": {"order_id": str}
            }
        
        Returns:
            {
                "allow": bool,
                "additional": {...}  # optional
            }
        """
        try:
            amount = params.get("amount", 0)
            account = params.get("account", {})
            order_id = account.get("order_id")
            
            if not order_id:
                raise PaymeError(-31051, "Order ID topilmadi")
            
            # Buyurtmani database'dan tekshirish
            # Bu qismni o'zingiz implement qilasiz
            # order = await get_order_by_id(order_id)
            
            # Misol:
            # if not order:
            #     raise PaymeError(-31052, "Buyurtma topilmadi")
            # 
            # if order.status != "pending":
            #     raise PaymeError(-31054, "Buyurtma aktiv emas")
            # 
            # expected_amount = int(order.total_amount * 100)  # tiyin
            # if amount != expected_amount:
            #     raise PaymeError(-31001, "Noto'g'ri summa")
            
            logger.info(f"Payme CheckPerform: order_id={order_id}, amount={amount}")
            
            return {
                "allow": True
            }
            
        except PaymeError:
            raise
        except Exception as e:
            logger.error(f"Payme CheckPerform xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def create_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        CreateTransaction - tranzaksiya yaratish
        
        Args:
            params: {
                "id": str,  # Payme transaction ID
                "time": int,  # timestamp
                "amount": int,  # tiyin
                "account": {"order_id": str}
            }
        
        Returns:
            {
                "create_time": int,
                "transaction": str,
                "state": int
            }
        """
        try:
            payme_id = params.get("id")
            payme_time = params.get("time")
            amount = params.get("amount", 0)
            account = params.get("account", {})
            order_id = account.get("order_id")
            
            if not order_id:
                raise PaymeError(-31051, "Order ID topilmadi")
            
            # Buyurtmani tekshirish
            # order = await get_order_by_id(order_id)
            
            # Tranzaksiyani database'ga saqlash
            # transaction = await create_payme_transaction(
            #     payme_id=payme_id,
            #     order_id=order_id,
            #     amount=amount / 100,  # so'mga qaytarish
            #     state=self.STATE_CREATED,
            #     create_time=payme_time
            # )
            
            logger.info(f"Payme CreateTransaction: {payme_id}, order={order_id}")
            
            return {
                "create_time": payme_time,
                "transaction": str(order_id),  # sizning internal ID
                "state": self.STATE_CREATED
            }
            
        except PaymeError:
            raise
        except Exception as e:
            logger.error(f"Payme CreateTransaction xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def verify_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapter-level payment verification wrapper for Payme callbacks."""
        return await self.check_perform_transaction(data)

    async def complete_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapter-level payment completion wrapper for Payme callbacks."""
        return await self.perform_transaction(data)

    async def perform_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        PerformTransaction - tranzaksiyani amalga oshirish
        
        Args:
            params: {
                "id": str  # Payme transaction ID
            }
        
        Returns:
            {
                "perform_time": int,
                "transaction": str,
                "state": int
            }
        """
        try:
            payme_id = params.get("id")
            
            # Tranzaksiyani topish
            # transaction = await get_payme_transaction(payme_id)
            
            # if not transaction:
            #     raise PaymeError(-31003, "Tranzaksiya topilmadi")
            
            # if transaction.state == self.STATE_COMPLETED:
            #     return {
            #         "perform_time": transaction.perform_time,
            #         "transaction": str(transaction.order_id),
            #         "state": self.STATE_COMPLETED
            #     }
            
            # Tranzaksiyani yakunlash
            perform_time = int(time.time() * 1000)
            
            # await update_transaction_state(
            #     payme_id=payme_id,
            #     state=self.STATE_COMPLETED,
            #     perform_time=perform_time
            # )
            
            # Buyurtmani "paid" holatiga o'tkazish
            # await update_order_status(transaction.order_id, "paid")
            
            logger.info(f"Payme PerformTransaction: {payme_id}")
            
            return {
                "perform_time": perform_time,
                "transaction": str(payme_id),
                "state": self.STATE_COMPLETED
            }
            
        except PaymeError:
            raise
        except Exception as e:
            logger.error(f"Payme PerformTransaction xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def cancel_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        CancelTransaction - tranzaksiyani bekor qilish
        
        Args:
            params: {
                "id": str,  # Payme transaction ID
                "reason": int  # Bekor qilish sababi
            }
        
        Returns:
            {
                "cancel_time": int,
                "transaction": str,
                "state": int
            }
        """
        try:
            payme_id = params.get("id")
            reason = params.get("reason", self.REASON_UNKNOWN)
            
            # Tranzaksiyani topish
            # transaction = await get_payme_transaction(payme_id)
            
            # if not transaction:
            #     raise PaymeError(-31003, "Tranzaksiya topilmadi")
            
            cancel_time = int(time.time() * 1000)
            
            # Holatga qarab bekor qilish
            # if transaction.state == self.STATE_CREATED:
            #     new_state = self.STATE_CANCELLED
            # elif transaction.state == self.STATE_COMPLETED:
            #     new_state = self.STATE_CANCELLED_AFTER_COMPLETE
            # else:
            #     # Allaqachon bekor qilingan
            #     return {
            #         "cancel_time": transaction.cancel_time,
            #         "transaction": str(transaction.order_id),
            #         "state": transaction.state
            #     }
            
            # await update_transaction_state(
            #     payme_id=payme_id,
            #     state=new_state,
            #     cancel_time=cancel_time,
            #     reason=reason
            # )
            
            logger.info(f"Payme CancelTransaction: {payme_id}, reason={reason}")
            
            return {
                "cancel_time": cancel_time,
                "transaction": str(payme_id),
                "state": self.STATE_CANCELLED
            }
            
        except PaymeError:
            raise
        except Exception as e:
            logger.error(f"Payme CancelTransaction xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def check_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        CheckTransaction - tranzaksiya holatini tekshirish
        
        Args:
            params: {
                "id": str  # Payme transaction ID
            }
        
        Returns:
            {
                "create_time": int,
                "perform_time": int,
                "cancel_time": int,
                "transaction": str,
                "state": int,
                "reason": int
            }
        """
        try:
            payme_id = params.get("id")
            
            # Tranzaksiyani topish
            # transaction = await get_payme_transaction(payme_id)
            
            # if not transaction:
            #     raise PaymeError(-31003, "Tranzaksiya topilmadi")
            
            # return {
            #     "create_time": transaction.create_time,
            #     "perform_time": transaction.perform_time or 0,
            #     "cancel_time": transaction.cancel_time or 0,
            #     "transaction": str(transaction.order_id),
            #     "state": transaction.state,
            #     "reason": transaction.reason or 0
            # }
            
            logger.info(f"Payme CheckTransaction: {payme_id}")
            
            # Misol javob
            return {
                "create_time": int(time.time() * 1000),
                "perform_time": 0,
                "cancel_time": 0,
                "transaction": str(payme_id),
                "state": self.STATE_CREATED,
                "reason": 0
            }
            
        except PaymeError:
            raise
        except Exception as e:
            logger.error(f"Payme CheckTransaction xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def get_statement(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        GetStatement - tranzaksiyalar ro'yxati
        
        Args:
            params: {
                "from": int,  # timestamp
                "to": int     # timestamp
            }
        
        Returns:
            {
                "transactions": [...]
            }
        """
        try:
            from_time = params.get("from")
            to_time = params.get("to")
            
            # Database'dan tranzaksiyalarni olish
            # transactions = await get_transactions_by_period(from_time, to_time)
            
            # result = []
            # for t in transactions:
            #     result.append({
            #         "id": t.payme_id,
            #         "time": t.create_time,
            #         "amount": int(t.amount * 100),
            #         "account": {"order_id": str(t.order_id)},
            #         "create_time": t.create_time,
            #         "perform_time": t.perform_time or 0,
            #         "cancel_time": t.cancel_time or 0,
            #         "transaction": str(t.order_id),
            #         "state": t.state,
            #         "reason": t.reason or 0
            #     })
            
            logger.info(f"Payme GetStatement: {from_time} - {to_time}")
            
            return {
                "transactions": []
            }
            
        except Exception as e:
            logger.error(f"Payme GetStatement xatosi: {e}")
            raise PaymeError(-31099, str(e))
    
    async def handle_request(
        self,
        method: str,
        params: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Payme so'rovni qayta ishlash
        
        Args:
            method: Metod nomi
            params: Parametrlar
            headers: HTTP headers
        
        Returns:
            Javob
        """
        # Autentifikatsiyani tekshirish
        if not self.check_authorization(headers):
            raise PaymeError(-32504, "Autentifikatsiya xato")
        
        # Metodga qarab handler'ni chaqirish
        handlers = {
            "CheckPerformTransaction": self.check_perform_transaction,
            "CreateTransaction": self.create_transaction,
            "PerformTransaction": self.perform_transaction,
            "CancelTransaction": self.cancel_transaction,
            "CheckTransaction": self.check_transaction,
            "GetStatement": self.get_statement,
        }
        
        handler = handlers.get(method)
        
        if not handler:
            raise PaymeError(-32601, f"Metod topilmadi: {method}")
        
        return await handler(params)


# Singleton instance
payme_payment = PaymePayment() if payment_settings.is_payme_enabled else None
