# handlers/admin/manual_topup.py
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command  
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.admin_states import ManualTopupStates
from bot.keyboards.inline_keyboards import get_admin_topup_keyboard
from bot.keyboards.main_menu import get_main_menu

from services.balance_service import BalanceService
from services.notification_service import NotificationService
from services.delivery_service import DeliveryService 

from config.settings import settings
from localization.texts import (
    MANUAL_TOPUP_SENT,
    ADMIN_MANUAL_REQUEST,
    MANUAL_TOPUP_APPROVED,
    MANUAL_TOPUP_REJECTED,
    ERROR_INVALID_SCREENSHOT,
    ERROR_GENERIC
)
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)


@router.message(Command("force_delivery"))
async def force_delivery_test(message: Message, session: AsyncSession, bot: Bot):
    """
    Команда запускает рассылку ПРЯМО СЕЙЧАС.
    Використання: /force_delivery morning (або afternoon, evening)
    """
    
    if message.from_user.id not in settings.ADMIN_IDS:
        return

    try:
       
        args = message.text.split()
        if len(args) < 2:
            await message.answer("⚠️ Вкажи слот: `morning`, `afternoon` або `evening`\nНаприклад: `/force_delivery morning`")
            return
            
        slot = args[1]
        await message.answer(f"🚀 Запускаю примусову розсилку для слоту: {slot}...")

        
        delivery_service = DeliveryService(session, bot)
        sent, failed = await delivery_service.deliver_valentines_for_slot(slot)

        await message.answer(
            f"✅ Розсилка завершена!\n"
            f"📨 Надіслано: {sent}\n"
            f"❌ Помилок: {failed}"
        )
        logger.info(f"Адмін {message.from_user.id} запустив force_delivery для {slot}")
        
    except Exception as e:
        logger.error(f"Помилка при force_delivery: {e}")
        await message.answer(f"❌ Критична помилка: {e}")


@router.message(ManualTopupStates.waiting_screenshot, F.photo | F.document)
async def handle_screenshot(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        full_name = message.from_user.full_name or "Користувач"
        username = message.from_user.username or "немає"
        
        if message.photo:
            photo_id = message.photo[-1].file_id
        elif message.document:
            photo_id = message.document.file_id
        else:
            await message.answer(text=ERROR_INVALID_SCREENSHOT)
            return
        
        await state.clear()
        
        await message.answer(
            text=MANUAL_TOPUP_SENT,
            reply_markup=get_main_menu()
        )
        
        admin_text = ADMIN_MANUAL_REQUEST.format(
            full_name=full_name,
            user_id=user_id,
            username=username
        )
        
        notification_service = NotificationService(bot)
        await notification_service.notify_admins(
            admin_ids=settings.ADMIN_IDS,
            text=admin_text,
            photo=photo_id,
            reply_markup=get_admin_topup_keyboard(user_id)
        )
        
        logger.info(f"Отримано скріншот від користувача {user_id}")
        
    except Exception as e:
        logger.error(f"Помилка в handle_screenshot: {e}")
        await message.answer(text=ERROR_GENERIC)

@router.message(ManualTopupStates.waiting_screenshot)
async def invalid_screenshot_type(message: Message):
    await message.answer(text=ERROR_INVALID_SCREENSHOT)


@router.callback_query(F.data.startswith("topup_approve:"))
async def admin_approve_topup(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    try:
        if callback.from_user.id not in settings.ADMIN_IDS:
            await callback.answer("Ви не адміністратор", show_alert=True)
            return
        
        parts = callback.data.split(":")
        if len(parts) != 3:
            await callback.answer("Невірний формат даних", show_alert=True)
            return
        
        user_id = int(parts[1])
        amount = int(parts[2])
        admin_id = callback.from_user.id
        
        balance_service = BalanceService(session)
        success = await balance_service.manual_topup(user_id, amount, admin_id)
        
        if not success:
            await callback.answer("Помилка або дублікат", show_alert=True)
            return
        
        notification_service = NotificationService(bot)
        await notification_service.send_message(
            user_id=user_id,
            text=MANUAL_TOPUP_APPROVED.format(amount=amount)
        )
        
        await callback.answer(f"✅ Нараховано {amount} валентинок")
        await callback.message.edit_reply_markup(reply_markup=None)
        
        logger.info(f"Адмін {admin_id} нарахував {amount} валентинок користувачу {user_id}")
        
    except Exception as e:
        logger.error(f"Помилка в admin_approve_topup: {e}")
        await callback.answer("Помилка обробки", show_alert=True)

@router.callback_query(F.data.startswith("topup_reject:"))
async def admin_reject_topup(callback: CallbackQuery, bot: Bot):
    try:
        if callback.from_user.id not in settings.ADMIN_IDS:
            await callback.answer("Ви не адміністратор", show_alert=True)
            return
        
        parts = callback.data.split(":")
        if len(parts) != 2:
            await callback.answer("Невірний формат даних", show_alert=True)
            return
        
        user_id = int(parts[1])
        
        notification_service = NotificationService(bot)
        await notification_service.send_message(
            user_id=user_id,
            text=MANUAL_TOPUP_REJECTED
        )
        
        await callback.answer("❌ Запит відхилено")
        await callback.message.edit_reply_markup(reply_markup=None)
        
        logger.info(f"Адмін {callback.from_user.id} відхилив запит користувача {user_id}")
        
    except Exception as e:
        logger.error(f"Помилка в admin_reject_topup: {e}")
        await callback.answer("Помилка обробки", show_alert=True)