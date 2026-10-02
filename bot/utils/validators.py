# bot/utils/validators.py
"""
Validation utility funksiyalar
"""
import re
import logging
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_user_checkout_state(user) -> dict:
    """Ensure the customer is fully registered, verified, and KYC-compliant before an order is accepted."""
    if user is None:
        return {"allowed": False, "missing": ["registration"], "reason": "user_not_found"}

    missing = []
    blocked = bool(getattr(user, "blocked", False))

    if blocked:
        return {"allowed": False, "missing": ["blocked"], "reason": "user_blocked"}

    role = str(getattr(user, "role", "guest") or "guest").lower()
    if role == "guest":
        missing.append("registration")

    if not getattr(user, "full_name", None) or not str(user.full_name).strip():
        missing.append("full_name")

    if not getattr(user, "phone_number", None):
        missing.append("phone_number")

    if not getattr(user, "is_phone_verified", False):
        missing.append("phone_verification")

    if not getattr(user, "is_kyc_verified", False):
        missing.append("kyc_verification")

    if not getattr(user, "passport_number", None) or not str(user.passport_number).strip():
        missing.append("passport_number")

    if not getattr(user, "address", None) or not str(user.address).strip():
        missing.append("delivery_address")

    return {
        "allowed": not missing,
        "missing": list(dict.fromkeys(missing)),
        "reason": "registration_required" if missing else "ok",
    }


def validate_order_payload(order_data: dict) -> dict:
    """Verify required cart, contact, and delivery data before order acceptance."""
    errors = []
    cart = order_data.get("cart") or {}
    phone = order_data.get("phone")
    delivery_address = order_data.get("delivery_address") or order_data.get("location")
    total_amount = float(order_data.get("total_amount", 0) or 0)

    if not cart or not any((v.get("qty", 0) or 0) > 0 for v in cart.values() if isinstance(v, dict)):
        errors.append("cart_empty")

    if phone is None or not str(phone).strip():
        errors.append("phone_missing")
    elif not validate_phone_number(str(phone))[0]:
        errors.append("phone_invalid")

    if not delivery_address or not str(delivery_address).strip():
        errors.append("delivery_address_missing")

    if total_amount <= 0:
        errors.append("amount_invalid")

    return {"allowed": not errors, "errors": list(dict.fromkeys(errors))}


def validate_phone_number(phone: str) -> Tuple[bool, Optional[str]]:
    """
    O'zbek telefon raqamini tekshirish
    
    Args:
        phone: Telefon raqam
    
    Returns:
        (is_valid, formatted_phone)
    
    Examples:
        >>> validate_phone_number("+998901234567")
        (True, "998901234567")
        >>> validate_phone_number("901234567")
        (True, "998901234567")
        >>> validate_phone_number("123")
        (False, None)
    """
    # Tozalash
    phone = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # + belgisini olib tashlash
    if phone.startswith("+"):
        phone = phone[1:]
    
    # 998 prefiksni qo'shish
    if len(phone) == 9:
        phone = "998" + phone
    
    # Pattern tekshirish
    # 998 + 2 xonali operator kodi + 7 xonali raqam
    pattern = r"^998(9[012345789]|6[125679]|7[01234569])\d{7}$"
    
    if re.match(pattern, phone):
        return True, phone
    
    return False, None


def validate_email(email: str) -> bool:
    """
    Email tekshirish
    
    Args:
        email: Email manzil
    
    Returns:
        is_valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    URL tekshirish
    
    Args:
        url: URL manzil
    
    Returns:
        is_valid
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_telegram_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Telegram username tekshirish
    
    Args:
        username: Telegram username
    
    Returns:
        (is_valid, formatted_username)
    
    Examples:
        >>> validate_telegram_username("@username")
        (True, "username")
        >>> validate_telegram_username("username")
        (True, "username")
    """
    # @ belgisini olib tashlash
    if username.startswith("@"):
        username = username[1:]
    
    # Pattern: 5-32 ta belgi, faqat harflar, raqamlar va _
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    
    if re.match(pattern, username):
        return True, username
    
    return False, None


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Parol kuchliligini tekshirish
    
    Args:
        password: Parol
    
    Returns:
        (is_valid, message)
    
    Shartlar:
        - Kamida 8 ta belgi
        - Kamida 1 ta katta harf
        - Kamida 1 ta kichik harf
        - Kamida 1 ta raqam
    """
    if len(password) < 8:
        return False, "Parol kamida 8 ta belgidan iborat bo'lishi kerak"
    
    if not re.search(r'[A-Z]', password):
        return False, "Parol kamida 1 ta katta harfni o'z ichiga olishi kerak"
    
    if not re.search(r'[a-z]', password):
        return False, "Parol kamida 1 ta kichik harfni o'z ichiga olishi kerak"
    
    if not re.search(r'\d', password):
        return False, "Parol kamida 1 ta raqamni o'z ichiga olishi kerak"
    
    return True, "Parol kuchli"


def validate_amount(amount: str) -> Tuple[bool, Optional[float]]:
    """
    Summa tekshirish
    
    Args:
        amount: Summa (string)
    
    Returns:
        (is_valid, amount_float)
    """
    try:
        # Vergul va bo'sh joylarni olib tashlash
        amount = amount.replace(",", "").replace(" ", "")
        
        # Float ga aylantirish
        amount_float = float(amount)
        
        # Musbat bo'lishi kerak
        if amount_float <= 0:
            return False, None
        
        return True, amount_float
        
    except ValueError:
        return False, None


def validate_quantity(quantity: str) -> Tuple[bool, Optional[float]]:
    """
    Miqdor tekshirish
    
    Args:
        quantity: Miqdor (string)
    
    Returns:
        (is_valid, quantity_float)
    """
    try:
        # Vergul va bo'sh joylarni olib tashlash
        quantity = quantity.replace(",", ".").replace(" ", "")
        
        # Float ga aylantirish
        quantity_float = float(quantity)
        
        # Musbat bo'lishi kerak
        if quantity_float <= 0:
            return False, None
        
        return True, quantity_float
        
    except ValueError:
        return False, None


def validate_otp_code(code: str) -> Tuple[bool, Optional[str]]:
    """
    OTP kodni tekshirish
    
    Args:
        code: OTP kod
    
    Returns:
        (is_valid, formatted_code)
    """
    # Tozalash
    code = code.strip().replace(" ", "").replace("-", "")
    
    # 6 xonali raqam bo'lishi kerak
    if len(code) != 6 or not code.isdigit():
        return False, None
    
    return True, code


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, Optional[datetime]]:
    """
    Sana tekshirish
    
    Args:
        date_str: Sana (string)
        format: Sana formati
    
    Returns:
        (is_valid, datetime_object)
    """
    try:
        date_obj = datetime.strptime(date_str, format)
        return True, date_obj
    except ValueError:
        return False, None


def validate_file_size(file_size: int, max_size_mb: int = 50) -> bool:
    """
    Fayl hajmini tekshirish
    
    Args:
        file_size: Fayl hajmi (bytes)
        max_size_mb: Maksimal hajm (MB)
    
    Returns:
        is_valid
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Fayl kengaytmasini tekshirish
    
    Args:
        filename: Fayl nomi
        allowed_extensions: Ruxsat etilgan kengaytmalar
    
    Returns:
        is_valid
    
    Example:
        >>> validate_file_extension("image.jpg", [".jpg", ".png"])
        True
    """
    extension = filename.lower().split(".")[-1]
    return f".{extension}" in [ext.lower() for ext in allowed_extensions]


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Kiritilgan matnni tozalash (XSS, injection)
    
    Args:
        text: Matn
        max_length: Maksimal uzunlik
    
    Returns:
        Tozalangan matn
    """
    # HTML teglarni olib tashlash
    text = re.sub(r'<[^>]+>', '', text)
    
    # Keraksiz bo'sh joylarni olib tashlash
    text = ' '.join(text.split())
    
    # Uzunlikni cheklash
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def validate_location(latitude: float, longitude: float) -> bool:
    """
    Koordinatalarni tekshirish
    
    Args:
        latitude: Kenglik
        longitude: Uzunlik
    
    Returns:
        is_valid
    """
    # Latitude: -90 dan 90 gacha
    # Longitude: -180 dan 180 gacha
    if not (-90 <= latitude <= 90):
        return False
    
    if not (-180 <= longitude <= 180):
        return False
    
    return True


def format_phone_display(phone: str) -> str:
    """
    Telefon raqamni chiroyli formatda ko'rsatish
    
    Args:
        phone: Telefon raqam (998901234567)
    
    Returns:
        Formatlangan raqam (+998 90 123 45 67)
    """
    if len(phone) == 12 and phone.startswith("998"):
        return f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:]}"
    
    return phone


def format_amount_display(amount: float) -> str:
    """
    Summani chiroyli formatda ko'rsatish
    
    Args:
        amount: Summa
    
    Returns:
        Formatlangan summa (1,000,000.00)
    """
    return f"{amount:,.2f}"


def validate_card_number(card_number: str) -> Tuple[bool, Optional[str]]:
    """
    Karta raqamini tekshirish (Luhn algoritmi)
    
    Args:
        card_number: Karta raqami
    
    Returns:
        (is_valid, formatted_number)
    """
    # Tozalash
    card_number = card_number.replace(" ", "").replace("-", "")
    
    # Faqat raqamlar
    if not card_number.isdigit():
        return False, None
    
    # 13-19 xona
    if not (13 <= len(card_number) <= 19):
        return False, None
    
    # Luhn algoritmi
    def luhn_check(card):
        digits = [int(d) for d in card]
        checksum = 0
        
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    if luhn_check(card_number):
        # Formatlash: **** **** **** 1234
        masked = "*" * (len(card_number) - 4) + card_number[-4:]
        formatted = " ".join([masked[i:i+4] for i in range(0, len(masked), 4)])
        return True, formatted
    
    return False, None
