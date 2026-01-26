# handlers/donate/donate.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.inline_keyboards import get_donate_keyboard
from bot.keyboards.main_menu import get_main_menu
from bot.states.admin_states import ManualTopupStates
from localization.texts import (
    DONATE_INSTRUCTION,
    DONATE_FORGOT_COMMENT,
    MENU_BUTTON_DONATE,
    ERROR_GENERIC
)
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)

@router.message(F.text == MENU_BUTTON_DONATE)
async def show_donate(message: Message):
    try:
        user_id = message.from_user.id
        code = str(user_id)
        
        text = DONATE_INSTRUCTION.format(code=code)
        
        await message.answer(
            text=text,
            reply_markup=get_donate_keyboard()
        )
    except Exception as e:
        logger.error(f"Помилка в show_donate: {e}")
        await message.answer(text=ERROR_GENERIC)

@router.callback_query(F.data == "donate_forgot")
async def donate_forgot_comment(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        await state.set_state(ManualTopupStates.waiting_screenshot)
        
        await callback.message.answer(
            text=DONATE_FORGOT_COMMENT,
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Помилка в donate_forgot_comment: {e}")
        await callback.message.answer(text=ERROR_GENERIC)