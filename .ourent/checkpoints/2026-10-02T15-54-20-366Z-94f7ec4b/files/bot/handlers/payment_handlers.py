# bot/handlers/payment_handlers.py
"""
To'lov handlerlar - Click va Payme webhooklar
"""
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from bot.db.database import get_session
from bot.db.models import Order
from bot.payment.click import click_payment
from bot.payment.payme import payme_payment
from bot.config import payment_settings

router = Router()
logger = logging.getLogger(__name__)


def resolve_order_for_payment(order) -> dict:
    """Return the real total amount attached to an order instead of a fake placeholder."""
    if order is None:
        return {"order_id": None, "order_number": None, "amount": 0.0, "status": None}

    if hasattr(order, "total_amount"):
        return {
            "order_id": getattr(order, "id", None),
            "order_number": getattr(order, "order_number", None),
            "amount": float(getattr(order, "total_amount", 0) or 0),
            "status": getattr(order, "status", None),
        }

    return {"order_id": order, "order_number": None, "amount": 0.0, "status": None}


async def get_order_for_payment(order_ref: str):
    """Load an actual order by numeric ID or order number from the database."""
    try:
        async with get_session() as session:
            target_id = int(str(order_ref).strip())
            result = await session.execute(select(Order).where(Order.id == target_id))
            order = result.scalar_one_or_none()
            if order is not None:
                return order
    except (ValueError, TypeError):
        pass

    async with get_session() as session:
        result = await session.execute(
            select(Order).where(Order.order_number == str(order_ref).strip())
        )
        return result.scalar_one_or_none()


# ==================== PAYMENT METHODS ====================

async def show_payment_methods(message: types.Message, order_id: str, amount: float):
    """
    To'lov usullarini ko'rsatish
    
    Args:
        message: Telegram message
        order_id: Buyurtma ID
        amount: Summa (so'm)
    """
    text = (
        f"💳 <b>To'lov usulini tanlang</b>\n\n"
        f"📦 Buyurtma: #{order_id}\n"
        f"💰 Summa: {amount:,.0f} so'm\n\n"
        f"To'lov usullaridan birini tanlang:"
    )
    
    keyboard = []
    
    # Click.uz
    if payment_settings.is_click_enabled and click_payment:
        keyboard.append([
            InlineKeyboardButton(
                text="💳 Click orqali to'lash",
                callback_data=f"pay_click:{order_id}"
            )
        ])
    
    # Payme
    if payment_settings.is_payme_enabled and payme_payment:
        keyboard.append([
            InlineKeyboardButton(
                text="💳 Payme orqali to'lash",
                callback_data=f"pay_payme:{order_id}"
            )
        ])
    
    # Naqd
    keyboard.append([
        InlineKeyboardButton(
            text="💵 Naqd pul",
            callback_data=f"pay_cash:{order_id}"
        )
    ])
    
    # Orqaga
    keyboard.append([
        InlineKeyboardButton(
            text="🔙 Orqaga",
            callback_data="back_to_cart"
        )
    ])
    
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await message.answer(text, reply_markup=kb)


# ==================== CLICK TO'LOVI ====================

@router.callback_query(F.data.startswith("pay_click:"))
async def process_click_payment(callback: types.CallbackQuery):
    """Click to'lovini boshlash"""
    try:
        order_ref = callback.data.split(":")[1]
        order = await get_order_for_payment(order_ref)
        if not order:
            await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
            return

        payment = resolve_order_for_payment(order)
        amount = payment["amount"]
        if amount <= 0:
            await callback.answer("❌ Noto'g'ri buyurtma summasi!", show_alert=True)
            return

        payment_url = click_payment.create_payment_url(
            amount=amount,
            order_id=str(payment["order_id"] or payment["order_number"] or order_ref),
            return_url=f"https://t.me/YourBot?start=order_{order_ref}",
            description=f"Buyurtma #{order_ref}"
        )
        
        text = (
            f"💳 <b>Click orqali to'lash</b>\n\n"
            f"📦 Buyurtma: #{order_id}\n"
            f"💰 Summa: {amount:,.0f} so'm\n\n"
            f"Quyidagi tugmani bosing va to'lovni amalga oshiring:"
        )
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 To'lovga o'tish", url=payment_url)],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_payment")]
        ])
        
        await callback.message.edit_text(text, reply_markup=kb)
        await callback.answer()
        
        logger.info(f"Click to'lov boshlandi: order={order_id}, amount={amount}")
        
    except Exception as e:
        logger.error(f"Click to'lov xatosi: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


@router.callback_query(F.data.startswith("check_click:"))
async def check_click_payment(callback: types.CallbackQuery):
    """Click to'lov holatini tekshirish"""
    try:
        order_id = callback.data.split(":")[1]
        
        # Click API orqali holat tekshirish
        status = await click_payment.check_payment_status(order_id)
        
        if status.get("error"):
            await callback.answer("❌ To'lov topilmadi!", show_alert=True)
            return
        
        # Holatga qarab xabar
        payment_status = status.get("status")
        
        if payment_status == "paid":
            text = (
                f"✅ <b>To'lov muvaffaqiyatli!</b>\n\n"
                f"📦 Buyurtma: #{order_id}\n"
                f"💳 To'lov: Click\n"
                f"✅ Holat: To'langan\n\n"
                f"Buyurtmangiz qabul qilindi!"
            )
        elif payment_status == "pending":
            text = (
                f"⏳ <b>To'lov kutilmoqda...</b>\n\n"
                f"📦 Buyurtma: #{order_id}\n"
                f"💳 To'lov: Click\n"
                f"⏳ Holat: Kutilmoqda\n\n"
                f"Iltimos, to'lovni yakunlang."
            )
        else:
            text = (
                f"❌ <b>To'lov bekor qilindi</b>\n\n"
                f"📦 Buyurtma: #{order_id}\n"
                f"💳 To'lov: Click\n"
                f"❌ Holat: Bekor qilingan"
            )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Click holat tekshirish xatosi: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


# ==================== PAYME TO'LOVI ====================

@router.callback_query(F.data.startswith("pay_payme:"))
async def process_payme_payment(callback: types.CallbackQuery):
    """Payme to'lovini boshlash"""
    try:
        order_ref = callback.data.split(":")[1]
        order = await get_order_for_payment(order_ref)
        if not order:
            await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
            return

        payment = resolve_order_for_payment(order)
        amount = payment["amount"]
        if amount <= 0:
            await callback.answer("❌ Noto'g'ri buyurtma summasi!", show_alert=True)
            return

        payment_url = payme_payment.generate_pay_link(
            amount=amount,
            order_id=str(payment["order_id"] or payment["order_number"] or order_ref),
            return_url=f"https://t.me/YourBot?start=order_{order_ref}",
            description=f"Buyurtma #{order_ref}"
        )
        
        text = (
            f"💳 <b>Payme orqali to'lash</b>\n\n"
            f"📦 Buyurtma: #{order_id}\n"
            f"💰 Summa: {amount:,.0f} so'm\n\n"
            f"Quyidagi tugmani bosing va to'lovni amalga oshiring:"
        )
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 To'lovga o'tish", url=payment_url)],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_payment")]
        ])
        
        await callback.message.edit_text(text, reply_markup=kb)
        await callback.answer()
        
        logger.info(f"Payme to'lov boshlandi: order={order_id}, amount={amount}")
        
    except Exception as e:
        logger.error(f"Payme to'lov xatosi: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


# ==================== NAQD TO'LOV ====================

@router.callback_query(F.data.startswith("pay_cash:"))
async def process_cash_payment(callback: types.CallbackQuery):
    """Naqd to'lov"""
    try:
        order_id = callback.data.split(":")[1]
        
        # Buyurtmani "cash" holatiga o'tkazish
        # await update_order_payment_method(order_id, "cash")
        
        text = (
            f"💵 <b>Naqd pul to'lovi</b>\n\n"
            f"📦 Buyurtma: #{order_id}\n"
            f"💵 To'lov usuli: Naqd pul\n\n"
            f"Yetkazib berish vaqtida to'lov qilasiz.\n\n"
            f"✅ Buyurtmangiz qabul qilindi!"
        )
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")]
        ])
        
        await callback.message.edit_text(text, reply_markup=kb)
        await callback.answer("✅ To'lov usuli saqlandi!")
        
        logger.info(f"Naqd to'lov tanlandi: order={order_id}")
        
    except Exception as e:
        logger.error(f"Naqd to'lov xatosi: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


# ==================== TO'LOV TARIXI ====================

@router.message(Command("payments"))
async def show_payment_history(message: types.Message, db_user):
    """To'lovlar tarixi"""
    try:
        # Database'dan foydalanuvchi to'lovlarini olish
        # payments = await get_user_payments(db_user.telegram_id)
        
        text = "💳 <b>To'lovlar tarixi</b>\n\n"
        
        # Misol uchun:
        payments = [
            {
                "id": "1",
                "order_id": "12345",
                "amount": 150000,
                "method": "click",
                "status": "paid",
                "date": "2026-04-01"
            },
            {
                "id": "2",
                "order_id": "12346",
                "amount": 200000,
                "method": "payme",
                "status": "paid",
                "date": "2026-04-02"
            }
        ]
        
        if not payments:
            text += "To'lovlar topilmadi."
        else:
            for payment in payments:
                method_emoji = "💳" if payment["method"] in ["click", "payme"] else "💵"
                status_emoji = "✅" if payment["status"] == "paid" else "⏳"
                
                text += (
                    f"{method_emoji} <b>Buyurtma #{payment['order_id']}</b>\n"
                    f"💰 {payment['amount']:,.0f} so'm\n"
                    f"{status_emoji} {payment['status'].upper()}\n"
                    f"📅 {payment['date']}\n\n"
                )
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="view_profile")]
        ])
        
        await message.answer(text, reply_markup=kb)
        
    except Exception as e:
        logger.error(f"To'lovlar tarixi xatosi: {e}")
        await message.answer("❌ Xatolik yuz berdi!")


# ==================== ORQAGA QAYTISH ====================

@router.callback_query(F.data == "back_to_payment")
async def back_to_payment(callback: types.CallbackQuery):
    """To'lov usullariga qaytish"""
    # Buyurtma ID ni callback data'dan olish kerak
    # Hozircha sodda misol
    await callback.message.edit_text(
        "To'lov usulini qaytadan tanlang...",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")]
        ])
    )
    await callback.answer()
