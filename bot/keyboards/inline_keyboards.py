# bot/keyboards/inline_keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization.texts import (
    BUTTON_DONATE_LINK,
    BUTTON_FORGOT_COMMENT,
    ADMIN_BUTTON_APPROVE_1,
    ADMIN_BUTTON_APPROVE_3,
    ADMIN_BUTTON_APPROVE_5,
    ADMIN_BUTTON_APPROVE_10,
    ADMIN_BUTTON_REJECT,
    SLOT_MORNING,
    SLOT_AFTERNOON,
    SLOT_EVENING
)
from config.constants import MONOBANK_JAR_LINK

def get_donate_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=BUTTON_DONATE_LINK, url=MONOBANK_JAR_LINK)],
        [InlineKeyboardButton(text=BUTTON_FORGOT_COMMENT, callback_data="donate_forgot")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_topup_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text=ADMIN_BUTTON_APPROVE_1, callback_data=f"topup_approve:{user_id}:1"),
            InlineKeyboardButton(text=ADMIN_BUTTON_APPROVE_3, callback_data=f"topup_approve:{user_id}:3")
        ],
        [
            InlineKeyboardButton(text=ADMIN_BUTTON_APPROVE_5, callback_data=f"topup_approve:{user_id}:5"),
            InlineKeyboardButton(text=ADMIN_BUTTON_APPROVE_10, callback_data=f"topup_approve:{user_id}:10")
        ],
        [
            InlineKeyboardButton(text=ADMIN_BUTTON_REJECT, callback_data=f"topup_reject:{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_delivery_slot_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=SLOT_MORNING, callback_data="slot:morning")],
        [InlineKeyboardButton(text=SLOT_AFTERNOON, callback_data="slot:afternoon")],
        [InlineKeyboardButton(text=SLOT_EVENING, callback_data="slot:evening")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)