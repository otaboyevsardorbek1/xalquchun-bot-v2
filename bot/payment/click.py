# bot/payment/click.py
"""
Click.uz to'lov tizimi integratsiyasi
"""
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import aiohttp
from bot.config import payment_settings

logger = logging.getLogger(__name__)


class ClickPayment:
    """Click.uz to'lov tizimi"""
    
    def __init__(self):
        self.merchant_id = payment_settings.click_merchant_id
        self.service_id = payment_settings.click_service_id
        self.secret_key = payment_settings.click_secret_key
        self.merchant_user_id = payment_settings.click_merchant_user_id
        self.api_url = "https://api.click.uz/v2/merchant"
    
    def generate_signature(self, **params) -> str:
        """
        Click imzo yaratish
        """
        # Parametrlarni tartiblash
        sorted_params = sorted(params.items())
        params_string = "".join(str(v) for k, v in sorted_params)
        params_string += self.secret_key
        
        # MD5 hash
        return hashlib.md5(params_string.encode()).hexdigest()
    
    def create_payment_url(
        self,
        amount: float,
        order_id: str,
        return_url: str = None,
        description: str = None
    ) -> str:
        """
        To'lov havolasi yaratish
        
        Args:
            amount: To'lov summasi
            order_id: Buyurtma ID
            return_url: Qaytish URL
            description: Izoh
        
        Returns:
            To'lov havolasi
        """
        params = {
            "service_id": self.service_id,
            "merchant_id": self.merchant_id,
            "amount": amount,
            "transaction_param": order_id,
            "return_url": return_url or "",
            "card_type": "01",  # Uzcard
        }
        
        # URL yaratish
        url_parts = []
        for key, value in params.items():
            url_parts.append(f"{key}={value}")
        
        url = f"https://my.click.uz/services/pay?{'&'.join(url_parts)}"
        
        logger.info(f"Click to'lov havolasi yaratildi: order_id={order_id}, amount={amount}")
        
        return url
    
    async def verify_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        To'lovni tasdiqlash (prepare)
        
        Args:
            data: Click'dan kelgan ma'lumotlar
        
        Returns:
            Javob
        """
        try:
            # Parametrlarni olish
            click_trans_id = data.get("click_trans_id")
            service_id = data.get("service_id")
            click_paydoc_id = data.get("click_paydoc_id")
            merchant_trans_id = data.get("merchant_trans_id")
            amount = float(data.get("amount", 0))
            action = data.get("action")
            sign_time = data.get("sign_time")
            sign_string = data.get("sign_string")
            
            # Imzoni tekshirish
            expected_sign = self.generate_signature(
                click_trans_id=click_trans_id,
                service_id=service_id,
                merchant_trans_id=merchant_trans_id,
                amount=amount,
                action=action,
                sign_time=sign_time
            )
            
            if sign_string != expected_sign:
                logger.error(f"Click imzo xato: {click_trans_id}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_prepare_id": 0,
                    "error": -1,
                    "error_note": "SIGN CHECK FAILED"
                }
            
            # Service ID tekshirish
            if str(service_id) != str(self.service_id):
                logger.error(f"Click service_id xato: {service_id}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_prepare_id": 0,
                    "error": -5,
                    "error_note": "SERVICE ID NOT FOUND"
                }
            
            # Action = 0 bo'lishi kerak (prepare)
            if int(action) != 0:
                logger.error(f"Click action xato: {action}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_prepare_id": 0,
                    "error": -3,
                    "error_note": "ACTION NOT FOUND"
                }
            
            # Buyurtmani tekshirish kerak (database)
            # Bu qismni o'zingiz implement qilasiz
            
            logger.info(f"Click to'lov tayyorlandi: {click_trans_id}")
            
            return {
                "click_trans_id": click_trans_id,
                "merchant_trans_id": merchant_trans_id,
                "merchant_prepare_id": int(merchant_trans_id),
                "error": 0,
                "error_note": "Success"
            }
            
        except Exception as e:
            logger.error(f"Click verify xatosi: {e}")
            return {
                "click_trans_id": data.get("click_trans_id"),
                "merchant_trans_id": data.get("merchant_trans_id"),
                "merchant_prepare_id": 0,
                "error": -9,
                "error_note": "SYSTEM ERROR"
            }
    
    async def complete_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        To'lovni yakunlash (complete)
        
        Args:
            data: Click'dan kelgan ma'lumotlar
        
        Returns:
            Javob
        """
        try:
            click_trans_id = data.get("click_trans_id")
            service_id = data.get("service_id")
            click_paydoc_id = data.get("click_paydoc_id")
            merchant_trans_id = data.get("merchant_trans_id")
            merchant_prepare_id = data.get("merchant_prepare_id")
            amount = float(data.get("amount", 0))
            action = data.get("action")
            sign_time = data.get("sign_time")
            sign_string = data.get("sign_string")
            error = data.get("error")
            
            # Imzoni tekshirish
            expected_sign = self.generate_signature(
                click_trans_id=click_trans_id,
                service_id=service_id,
                merchant_trans_id=merchant_trans_id,
                merchant_prepare_id=merchant_prepare_id,
                amount=amount,
                action=action,
                sign_time=sign_time
            )
            
            if sign_string != expected_sign:
                logger.error(f"Click imzo xato: {click_trans_id}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_confirm_id": 0,
                    "error": -1,
                    "error_note": "SIGN CHECK FAILED"
                }
            
            # Action = 1 bo'lishi kerak (complete)
            if int(action) != 1:
                logger.error(f"Click action xato: {action}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_confirm_id": 0,
                    "error": -3,
                    "error_note": "ACTION NOT FOUND"
                }
            
            # Error kodini tekshirish
            if int(error) < 0:
                logger.error(f"Click to'lov xato: {error}")
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_confirm_id": 0,
                    "error": -6,
                    "error_note": "TRANSACTION FAILED"
                }
            
            # To'lovni database'ga yozish kerak
            # Bu qismni o'zingiz implement qilasiz
            
            logger.info(f"Click to'lov yakunlandi: {click_trans_id}")
            
            return {
                "click_trans_id": click_trans_id,
                "merchant_trans_id": merchant_trans_id,
                "merchant_confirm_id": int(merchant_trans_id),
                "error": 0,
                "error_note": "Success"
            }
            
        except Exception as e:
            logger.error(f"Click complete xatosi: {e}")
            return {
                "click_trans_id": data.get("click_trans_id"),
                "merchant_trans_id": data.get("merchant_trans_id"),
                "merchant_confirm_id": 0,
                "error": -9,
                "error_note": "SYSTEM ERROR"
            }
    
    async def check_payment_status(self, merchant_trans_id: str) -> Dict[str, Any]:
        """
        To'lov holatini tekshirish
        
        Args:
            merchant_trans_id: Buyurtma ID
        
        Returns:
            To'lov holati
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/invoice/status"
                params = {
                    "service_id": self.service_id,
                    "merchant_trans_id": merchant_trans_id
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Click holat: {merchant_trans_id} = {data}")
                        return data
                    else:
                        logger.error(f"Click API xato: {response.status}")
                        return {"error": "API_ERROR"}
                        
        except Exception as e:
            logger.error(f"Click status xatosi: {e}")
            return {"error": str(e)}


# Singleton instance
click_payment = ClickPayment() if payment_settings.is_click_enabled else None
