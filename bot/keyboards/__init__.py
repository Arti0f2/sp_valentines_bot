# bot/keyboards/__init__.py
# всі клавіатури

from bot.keyboards.main_menu import get_main_menu
from bot.keyboards.inline_keyboards import (
    get_donate_keyboard,
    get_admin_topup_keyboard
)

__all__ = [
    'get_main_menu',
    'get_donate_keyboard',
    'get_admin_topup_keyboard'
]