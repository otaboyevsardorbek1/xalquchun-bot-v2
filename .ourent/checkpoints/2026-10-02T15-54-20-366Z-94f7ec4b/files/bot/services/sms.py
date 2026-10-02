# bot/services/sms.py
"""
SMS yuborish xizmatlari
Eskiz.uz va PlayMobile integratsiyasi
"""
import random
import logging
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import aiohttp
from bot.config import sms_settings

logger = logging.getLogger(__name__)


class SMSProvider:
    """SMS yuborish uchun asosiy klass"""
    
    async def send_sms(self, phone: str, message: str) -> bool:
        """SMS yuborish"""
        raise NotImplementedError
    
    async def send_otp(self, phone: str, code: str = None) -> Optional[str]:
        """OTP kod yuborish"""
        if not code:
            code = self.generate_otp()
        
        message = f"Tasdiqlash kodi: {code}\n\nXalqUchun Bot"
        success = await self.send_sms(phone, message)
        
        return code if success else None
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """OTP kod generatsiya qilish"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """
        Telefon raqamni formatlash
        +998901234567 -> 998901234567
        """
        phone = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if phone.startswith("+"):
            phone = phone[1:]
        return phone


class EskizSMS(SMSProvider):
    """Eskiz.uz SMS provider"""
    
    def __init__(self):
        self.email = sms_settings.eskiz_email
        self.password = sms_settings.eskiz_password
        self.api_url = "https://notify.eskiz.uz/api"
        self.token = None
        self.token_expires = None
    
    async def get_token(self) -> Optional[str]:
        """API token olish"""
        try:
            # Token hali yaroqli bo'lsa, qaytarish
            if self.token and self.token_expires and datetime.now() < self.token_expires:
                return self.token
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/auth/login"
                data = {
                    "email": self.email,
                    "password": self.password
                }
                
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.token = result.get("data", {}).get("token")
                        # Token 30 kun yaroqli
                        self.token_expires = datetime.now() + timedelta(days=29)
                        
                        logger.info("Eskiz.uz token olindi")
                        return self.token
                    else:
                        logger.error(f"Eskiz.uz token olish xatosi: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Eskiz.uz token xatosi: {e}")
            return None
    
    async def send_sms(self, phone: str, message: str) -> bool:
        """
        SMS yuborish
        
        Args:
            phone: Telefon raqam (998901234567)
            message: Xabar matni
        
        Returns:
            True agar yuborilsa
        """
        try:
            token = await self.get_token()
            if not token:
                logger.error("Eskiz.uz token yo'q")
                return False
            
            phone = self.format_phone(phone)
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/message/sms/send"
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                data = {
                    "mobile_phone": phone,
                    "message": message,
                    "from": "4546",  # Eskiz.uz dan berilgan raqam
                    "callback_url": ""  # Optional
                }
                
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Eskiz SMS yuborildi: {phone}")
                        return True
                    else:
                        error = await response.text()
                        logger.error(f"Eskiz SMS xato: {response.status}, {error}")
                        return False
                        
        except Exception as e:
            logger.error(f"Eskiz SMS yuborish xatosi: {e}")
            return False
    
    async def get_balance(self) -> Optional[float]:
        """Balansni tekshirish"""
        try:
            token = await self.get_token()
            if not token:
                return None
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/user/get-limit"
                headers = {"Authorization": f"Bearer {token}"}
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        balance = result.get("data", {}).get("balance", 0)
                        logger.info(f"Eskiz balans: {balance}")
                        return float(balance)
                    return None
                    
        except Exception as e:
            logger.error(f"Eskiz balans xatosi: {e}")
            return None


class PlayMobileSMS(SMSProvider):
    """PlayMobile SMS provider"""
    
    def __init__(self):
        self.login = sms_settings.playmobile_login
        self.password = sms_settings.playmobile_password
        self.api_url = "https://send.smsxabar.uz/broker-api"
    
    async def send_sms(self, phone: str, message: str) -> bool:
        """
        SMS yuborish
        
        Args:
            phone: Telefon raqam (998901234567)
            message: Xabar matni
        
        Returns:
            True agar yuborilsa
        """
        try:
            phone = self.format_phone(phone)
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/send"
                params = {
                    "login": self.login,
                    "password": self.password,
                    "data": message,
                    "numbers": phone
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        result = await response.text()
                        # PlayMobile javob formati: "ok,id"
                        if result.startswith("ok"):
                            logger.info(f"PlayMobile SMS yuborildi: {phone}")
                            return True
                        else:
                            logger.error(f"PlayMobile xato: {result}")
                            return False
                    else:
                        logger.error(f"PlayMobile API xato: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"PlayMobile SMS yuborish xatosi: {e}")
            return False
    
    async def get_balance(self) -> Optional[float]:
        """Balansni tekshirish"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/balance"
                params = {
                    "login": self.login,
                    "password": self.password
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        balance = await response.text()
                        logger.info(f"PlayMobile balans: {balance}")
                        return float(balance)
                    return None
                    
        except Exception as e:
            logger.error(f"PlayMobile balans xatosi: {e}")
            return None


class SMSService:
    """SMS xizmati - barcha providerlarni boshqaradi"""
    
    def __init__(self):
        self.providers = []
        
        # Eskiz.uz
        if sms_settings.is_eskiz_enabled:
            self.providers.append(EskizSMS())
            logger.info("✅ Eskiz.uz SMS provider yoqildi")
        
        # PlayMobile
        if sms_settings.is_playmobile_enabled:
            self.providers.append(PlayMobileSMS())
            logger.info("✅ PlayMobile SMS provider yoqildi")
        
        if not self.providers:
            logger.warning("⚠️ Hech qanday SMS provider yoqilmagan!")
    
    async def send_sms(self, phone: str, message: str) -> bool:
        """
        SMS yuborish (birinchi providerdan)
        
        Args:
            phone: Telefon raqam
            message: Xabar matni
        
        Returns:
            True agar yuborilsa
        """
        if not self.providers:
            logger.error("SMS provider mavjud emas!")
            return False
        
        # Birinchi providerdan yuborish
        provider = self.providers[0]
        return await provider.send_sms(phone, message)
    
    async def send_sms_with_fallback(self, phone: str, message: str) -> bool:
        """
        SMS yuborish (fallback bilan)
        Agar birinchi provider ishlamasa, keyingisiga o'tadi
        
        Args:
            phone: Telefon raqam
            message: Xabar matni
        
        Returns:
            True agar hech bo'lmaganda bitta providerdan yuborilsa
        """
        if not self.providers:
            logger.error("SMS provider mavjud emas!")
            return False
        
        for i, provider in enumerate(self.providers, 1):
            try:
                logger.info(f"SMS yuborish urinish {i}/{len(self.providers)}")
                success = await provider.send_sms(phone, message)
                if success:
                    return True
                
                # Keyingi providerga o'tishdan oleh kutish
                if i < len(self.providers):
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Provider {i} xatosi: {e}")
                continue
        
        logger.error("Barcha providerlar ishlamadi!")
        return False
    
    async def send_otp(self, phone: str, code: str = None) -> Optional[str]:
        """
        OTP kod yuborish
        
        Args:
            phone: Telefon raqam
            code: OTP kod (optional, avtomatik generatsiya qilinadi)
        
        Returns:
            OTP kod agar yuborilsa, aks holda None
        """
        if not self.providers:
            logger.error("SMS provider mavjud emas!")
            return None
        
        provider = self.providers[0]
        return await provider.send_otp(phone, code)
    
    async def check_balance(self) -> Dict[str, float]:
        """
        Barcha providerlarning balansini tekshirish
        
        Returns:
            {provider_name: balance}
        """
        balances = {}
        
        for provider in self.providers:
            try:
                balance = await provider.get_balance()
                name = provider.__class__.__name__
                balances[name] = balance
            except Exception as e:
                logger.error(f"Balans tekshirish xatosi: {e}")
                continue
        
        return balances


# Singleton instance
sms_service = SMSService()


# ==================== OTP CACHE ====================

class OTPCache:
    """OTP kodlarni xotirada saqlash"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = 300  # 5 daqiqa
    
    def set(self, phone: str, code: str):
        """OTP kodni saqlash"""
        self.cache[phone] = {
            "code": code,
            "expires": datetime.now() + timedelta(seconds=self.ttl),
            "attempts": 0
        }
        logger.info(f"OTP saqlandi: {phone}")
    
    def get(self, phone: str) -> Optional[str]:
        """OTP kodni olish"""
        data = self.cache.get(phone)
        
        if not data:
            return None
        
        # Muddati o'tgan bo'lsa
        if datetime.now() > data["expires"]:
            del self.cache[phone]
            logger.info(f"OTP muddati o'tgan: {phone}")
            return None
        
        return data["code"]
    
    def verify(self, phone: str, code: str) -> bool:
        """OTP kodni tekshirish"""
        data = self.cache.get(phone)
        
        if not data:
            logger.warning(f"OTP topilmadi: {phone}")
            return False
        
        # Muddati o'tgan bo'lsa
        if datetime.now() > data["expires"]:
            del self.cache[phone]
            logger.warning(f"OTP muddati o'tgan: {phone}")
            return False
        
        # Urinishlar sonini oshirish
        data["attempts"] += 1
        
        # Maksimal urinishlar (3 marta)
        if data["attempts"] > 3:
            del self.cache[phone]
            logger.warning(f"OTP urinishlar soni oshib ketdi: {phone}")
            return False
        
        # Tekshirish
        if data["code"] == code:
            del self.cache[phone]
            logger.info(f"OTP to'g'ri: {phone}")
            return True
        
        logger.warning(f"OTP noto'g'ri: {phone}")
        return False
    
    def delete(self, phone: str):
        """OTP kodni o'chirish"""
        if phone in self.cache:
            del self.cache[phone]
            logger.info(f"OTP o'chirildi: {phone}")
    
    def clear_expired(self):
        """Muddati o'tgan kodlarni tozalash"""
        now = datetime.now()
        expired = [
            phone for phone, data in self.cache.items()
            if now > data["expires"]
        ]
        
        for phone in expired:
            del self.cache[phone]
        
        if expired:
            logger.info(f"Tozalandi: {len(expired)} ta muddati o'tgan OTP")


# Singleton instance
otp_cache = OTPCache()


# ==================== BACKGROUND TASK ====================

async def otp_cleanup_task():
    """OTP cache'ni tozalash task"""
    while True:
        try:
            await asyncio.sleep(60)  # Har daqiqada
            otp_cache.clear_expired()
        except Exception as e:
            logger.error(f"OTP cleanup xatosi: {e}")
