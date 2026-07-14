# bot/keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from localization.texts import MENU_BUTTON_SEND, MENU_BUTTON_DONATE, MENU_BUTTON_HELP

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MENU_BUTTON_SEND)],
        [KeyboardButton(text=MENU_BUTTON_DONATE)],
        [KeyboardButton(text=MENU_BUTTON_HELP)]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Обери дію..."
    )