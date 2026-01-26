# handlers/common/help.py
from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.main_menu import get_main_menu
from localization.texts import HOW_IT_WORKS, MENU_BUTTON_HELP

router = Router()

@router.message(F.text == MENU_BUTTON_HELP)
async def show_help(message: Message):
    await message.answer(
        text=HOW_IT_WORKS,
        reply_markup=get_main_menu()
    )