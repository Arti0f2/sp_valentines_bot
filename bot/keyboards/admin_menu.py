# bot/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="💰 Ручне поповнення")],
        [KeyboardButton(text="📢 Розсилка")],
        [KeyboardButton(text="◀️ Головне меню")]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Оберіть дію..."
    )