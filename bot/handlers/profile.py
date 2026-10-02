# bot/handlers/profile.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from bot.keyboards.main import get_main_menu, get_back_button
from aiogram.types import Message, CallbackQuery
from typing import Union
from bot.db.database import get_session
from bot.db.models import User, Transaction
from bot.services.audit import AuditLogService
from bot.services.kyc import KYCService, KYCSubmission
from bot.utils.referral import get_user_by_tid
from bot.utils.helpers import validate_uz_phone, format_phone_for_display, format_price
from bot.data import ADMIN_IDS
import logging

router = Router()
logger = logging.getLogger(__name__)

class ProfileState(StatesGroup):
    waiting_for_new_phone = State()


class KYCProfileState(StatesGroup):
    waiting_for_kyc = State()

@router.message(Command("profile"))
@router.callback_query(F.data == "view_profile")
async def cmd_profile(event:Union[ Message ,CallbackQuery]):
    """Profil ma'lumotlarini ko'rsatish"""
    try:
        user_id = event.from_user.id
        
        # Admin tekshirish
        is_admin = user_id in ADMIN_IDS
        
        async with get_session() as session:
            user = await get_user_by_tid(session, user_id)
            
            if not user:
                text = "❌ Siz roʻyxatdan oʻtmagan. /start ni bosing."
                if isinstance(event, types.Message):
                    await event.answer(text)
                else:
                    await event.message.answer(text)
                    await event.answer()
                return
            
            # Tranzaksiyalar soni va balans
            transactions_count = await session.execute(
                select(Transaction).where(Transaction.user_telegram_id == user_id)
            )
            transactions_count = len(transactions_count.scalars().all())
        
        # Profil ma'lumotlari
        phone_display = format_phone_for_display(user.phone_number) if user.phone_number else "❌"
        balance_str = format_price(user.balance)
        
        # Rolga qarab emoji
        role_emoji = {
            'owner': '👑', 'admin': '🔰', 'manager': '⭐',
            'worker': '⚙️', 'diller': '💎', 'dastafka': '🔧', 'guest': '👤'
        }.get(user.role, '👤')
        
        kyc_status = "✅ Tasdiqlangan" if user.is_kyc_verified else "⏳ Tasdiqlanish kutilmoqda"
        kyc_details = "" if user.is_kyc_verified else "\n🔐 *KYC:* ma'lumotlarni to'ldiring va tasdiqlash uchun yuboring."

        text = f"""
{role_emoji} *SHAXSIY PROFIL* {role_emoji}
{'-' * 30}

🆔 *ID:* `{user.telegram_id}`
📝 *Ism:* {user.full_name or '—'}
👤 *Username:* @{user.username or '—'}
📞 *Telefon:* {phone_display}
📍 *Manzil:* {user.address or '—'}
🪪 *Passport:* {user.passport_number or '—'}
🎭 *Rol:* {user.role}
💰 *Balans:* {balance_str} so'm
👥 *Takliflar:* {user.referrals_count} ta
📊 *Tranzaksiyalar:* {transactions_count} ta
🔒 *Bloklangan:* {'✅' if not user.blocked else '❌'}
🆔 *KYC holati:* {kyc_status}{kyc_details}
📅 *Ro'yxatdan o'tgan:* {user.created_at.strftime('%d.%m.%Y')}
        """
        
        # Tugmalar
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Telefonni yangilash", callback_data="update_phone")],
            [InlineKeyboardButton(text="🆔 KYC ni yakunlash", callback_data="start_kyc")],
            [InlineKeyboardButton(text="💰 Balans", callback_data="view_balance")],
            [InlineKeyboardButton(text="📜 Tranzaksiyalar", callback_data="view_transactions")],
            [InlineKeyboardButton(text="👥 Referallar", callback_data="view_referrals")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ])
        
        if isinstance(event, types.Message):
            await event.answer(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await event.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
            await event.answer()
            
    except Exception as e:
        logger.error(f"Profil ko'rsatishda xato: {e}")
        error_msg = "❌ Xatolik yuz berdi."
        if isinstance(event, types.Message):
            await event.answer(error_msg)
        else:
            await event.message.answer(error_msg)
            await event.answer()

@router.callback_query(F.data == "start_kyc")
async def start_kyc(callback: types.CallbackQuery, state: FSMContext):
    """Start the real customer KYC submission flow."""
    try:
        await callback.message.answer(
            "🆔 *KYC ma'lumotlarini kiriting*\n\n"
            "Quyidagi formatda yozing:\n"
            "`Ism Familiya\nTelefon\nManzil\nPassport raqami\nID / pasport ma'lumotlari`\n\n"
            "Masalan:\n"
            "`Ali Valiev\n+998901234567\nToshkent, Yunusobod 15-uy\nAB1234567\nID seriyasi va ma'lumotlar`",
            parse_mode="Markdown",
        )
        await state.set_state(KYCProfileState.waiting_for_kyc)
        await callback.answer()
    except Exception as e:
        logger.error(f"KYC boshlashda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.message(KYCProfileState.waiting_for_kyc)
async def submit_kyc(message: types.Message, state: FSMContext):
    """Validate and save KYC data before checkout is allowed."""
    try:
        lines = [line.strip() for line in message.text.splitlines() if line.strip()]
        if len(lines) < 5:
            await message.answer("❌ KYC ma'lumotlari yetarli emas. Qayta kiriting.")
            return

        submission = KYCSubmission(
            full_name=lines[0],
            phone_number=lines[1],
            address=" ".join(lines[2:-2]) if len(lines) > 5 else lines[2],
            passport_number=lines[-2],
            id_document_data=lines[-1],
        )

        validation = KYCService.validate_submission(submission)
        if not validation["allowed"]:
            await message.answer(
                "❌ KYC ma'lumotlari to'liq emas. Kerakli maydonlar: "
                + ", ".join(validation["errors"]),
            )
            return

        async with get_session() as session:
            user = await get_user_by_tid(session, message.from_user.id)
            if user:
                user.full_name = submission.full_name
                user.phone_number = submission.phone_number
                user.address = submission.address
                user.passport_number = submission.passport_number
                user.id_document_data = submission.id_document_data
                user.is_kyc_verified = True
                user.kyc_status = "verified"
                user.kyc_verified_at = __import__("datetime").datetime.utcnow()
                await session.commit()

                AuditLogService.record_event(
                    session,
                    event_type="kyc_verified",
                    entity_type="user",
                    entity_id=user.telegram_id,
                    user_telegram_id=user.telegram_id,
                    admin_telegram_id=None,
                    action="approved",
                    details={"status": "verified"},
                )

        await message.answer(
            "✅ KYC ma'lumotlari qabul qilindi va tasdiqlandi.\n\nEndi buyurtma berish mumkin.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.clear()
    except Exception as e:
        logger.error(f"KYC yuborishda xato: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()


@router.callback_query(F.data == "update_phone")
async def update_phone_start(callback: types.CallbackQuery, state: FSMContext):
    """Telefon raqamni yangilashni boshlash"""
    try:
        await callback.message.delete()
        
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        
        await callback.message.answer(
            "📞 *Telefon raqamni yangilash*\n\n"
            "Yangi telefon raqamingizni yuboring:\n"
            "• Pastdagi tugma orqali\n"
            "• Yoki qo'lda kiriting: `+998 XX XXX XX XX`",
            parse_mode="Markdown",
            reply_markup=kb
        )
        
        await state.set_state(ProfileState.waiting_for_new_phone)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Telefon yangilashni boshlashda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.message(ProfileState.waiting_for_new_phone, F.contact)
async def update_phone_contact(message: types.Message, state: FSMContext):
    """Telefon raqamni kontakt orqali yangilash"""
    try:
        phone = message.contact.phone_number
        is_valid, cleaned = validate_uz_phone(phone)
        
        if not is_valid:
            await message.answer(
                "❌ Notoʻgʻri Oʻzbekiston raqami. Iltimos, qayta urinib koʻring."
            )
            return
        
        # Telefon raqamni yangilash
        async with get_session() as session:
            user = await get_user_by_tid(session, message.from_user.id)
            if user:
                user.phone_number = cleaned
                user.is_phone_verified = True
                await session.commit()
        
        await message.answer(
            f"✅ Telefon raqam yangilandi!\n\nYangi raqam: {format_phone_for_display(cleaned)}",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardRemove()
        )
        
        # Profilni ko'rsatish
        await cmd_profile(message)
        await state.clear()
        
    except Exception as e:
        logger.error(f"Telefon yangilashda xato: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()

@router.message(ProfileState.waiting_for_new_phone)
async def update_phone_text(message: types.Message, state: FSMContext):
    """Telefon raqamni matn orqali yangilash"""
    try:
        phone = message.text.strip()
        is_valid, cleaned = validate_uz_phone(phone)
        
        if not is_valid:
            await message.answer(
                "❌ Notoʻgʻri format. Iltimos, `+998 XX XXX XX XX` formatida kiriting.",
                parse_mode="Markdown"
            )
            return
        
        # Telefon raqamni yangilash
        async with get_session() as session:
            user = await get_user_by_tid(session, message.from_user.id)
            if user:
                user.phone_number = cleaned
                user.is_phone_verified = True
                await session.commit()
        
        await message.answer(
            f"✅ Telefon raqam yangilandi!\n\nYangi raqam: {format_phone_for_display(cleaned)}",
            parse_mode="Markdown"
        )
        
        # Profilni ko'rsatish
        await cmd_profile(message)
        await state.clear()
        
    except Exception as e:
        logger.error(f"Telefon yangilashda xato: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()

@router.callback_query(F.data == "view_balance")
async def view_balance(callback: types.CallbackQuery):
    """Balansni ko'rsatish"""
    try:
        async with get_session() as session:
            user = await get_user_by_tid(session, callback.from_user.id)
            balance = user.balance if user else 0.0
        
        balance_str = format_price(balance)
        
        text = f"""
💰 *BALANSINGIZ* 💰
{'-' * 30}

Joriy balans: *{balance_str} so'm*

Pul yechish uchun /withdraw [summa] buyrug'idan foydalaning.
Masalan: `/withdraw 50000`
        """
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 Pul yechish", callback_data="withdraw_start")],
            [InlineKeyboardButton(text="📜 Tranzaksiyalar", callback_data="view_transactions")],
            [InlineKeyboardButton(text="🔙 Profil", callback_data="view_profile")]
        ])
        
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Balans ko'rsatishda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "view_transactions")
async def view_transactions(callback: types.CallbackQuery):
    """Tranzaksiyalarni ko'rsatish"""
    try:
        from bot.utils.referral import list_user_transactions
        
        txs = await list_user_transactions(callback.from_user.id)
        
        if not txs:
            text = "📭 *Tranzaksiyalar topilmadi.*"
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Profil", callback_data="view_profile")]
            ])
            await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
            await callback.answer()
            return
        
        lines = ["📜 *TRANZAKSIYALAR TARIXI* 📜\n"]
        
        for t in txs[:10]:  # Oxirgi 10 ta
            status_emoji = {
                "approved": "✅",
                "pending": "⏳",
                "declined": "❌"
            }.get(t.status, "❓")
            
            date_str = t.created_at.strftime('%d.%m.%Y %H:%M')
            amount_str = format_price(t.amount)
            
            lines.append(
                f"{status_emoji} `{t.id}` | {t.type}\n"
                f"   💰 {amount_str} so'm | {t.status}\n"
                f"   🕐 {date_str}"
            )
        
        if len(txs) > 10:
            lines.append(f"\n... va yana {len(txs) - 10} ta tranzaksiya")
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Balans", callback_data="view_balance")],
            [InlineKeyboardButton(text="🔙 Profil", callback_data="view_profile")]
        ])
        
        await callback.message.edit_text("\n\n".join(lines), parse_mode="Markdown", reply_markup=kb)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Tranzaksiyalarni ko'rsatishda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "view_referrals")
async def view_referrals(callback: types.CallbackQuery):
    """Referallarni ko'rsatish"""
    try:
        from bot.utils.referral import get_children, count_downline
        
        user_id = callback.from_user.id
        children = await get_children(user_id)
        total_downline = await count_downline(user_id)
        
        text = f"""
👥 *REFERALLAR* 👥
{'-' * 30}

👤 Sizning referal daraxtingiz:
• Bevosita taklif qilganlar: {len(children)} ta
• Barcha avlodlar: {total_downline} ta

🔗 *Referal havolangiz:*
`https://t.me/{(await callback.bot.get_me()).username}?start={user_id}`

🌟 *Bonus tizimi:*
• 1-daraja: 100 so'm
• 2-daraja: 50 so'm
• 3-daraja: 25 so'm
• 4-daraja: 10 so'm
• 5-daraja: 5 so'm
        """
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌳 Referal daraxti", callback_data="view_tree")],
            [InlineKeyboardButton(text="🖼 Daraxt rasmi", callback_data="view_tree_img")],
            [InlineKeyboardButton(text="🔙 Profil", callback_data="view_profile")]
        ])
        
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Referallarni ko'rsatishda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "view_tree")
async def view_tree(callback: types.CallbackQuery):
    """Referal daraxtini matn ko'rinishida ko'rsatish"""
    try:
        from bot.utils.referral import build_tree_text
        from bot.data import MAX_TREE_DEPTH
        
        await callback.answer("⏳ Daraxt yaratilmoqda...")
        
        tree = await build_tree_text(callback.from_user.id, max_depth=MAX_TREE_DEPTH)
        
        if not tree:
            text = "📭 Siz hali hech kimni taklif qilmagansiz."
        else:
            text = f"🌳 *SIZNING REFERAL DARAXTINGIZ*\n\n`{tree}`"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🖼 Rasm ko'rinishida", callback_data="view_tree_img")],
            [InlineKeyboardButton(text="🔙 Referallar", callback_data="view_referrals")]
        ])
        
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
        
    except Exception as e:
        logger.error(f"Referal daraxtini ko'rsatishda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "view_tree_img")
async def view_tree_img(callback: types.CallbackQuery):
    """Referal daraxtini rasm ko'rinishida ko'rsatish"""
    try:
        from bot.handlers.referral import cmd_treeimg
        
        # Rasm yaratish uchun maxsus handler
        await callback.answer("⏳ Rasm yaratilmoqda...")
        
        # Bu yerda rasm yaratish kodi
        await callback.message.answer("🖼 Rasm yaratish funksiyasi ishlab chiqilmoqda...")
        
    except Exception as e:
        logger.error(f"Referal daraxti rasmini ko'rsatishda xato: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)