# handlers/valentines/send_valentine.py
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states.sending_states import SendValentineStates
from bot.keyboards.inline_keyboards import get_delivery_slot_keyboard
from bot.keyboards.main_menu import get_main_menu
from services.valentine_service import ValentineService
from services.balance_service import BalanceService
from config.constants import MAX_VALENTINE_TEXT_LENGTH, VALENTINE_COST
from localization.texts import (
    SEND_VALENTINE_START,
    SEND_VALENTINE_MESSAGE,
    SEND_VALENTINE_SLOT,
    VALENTINE_CREATED,
    ERROR_INVALID_USERNAME,
    ERROR_SELF_SEND,
    ERROR_MESSAGE_TOO_LONG,
    ERROR_INSUFFICIENT_BALANCE,
    ERROR_GENERIC,
    MENU_BUTTON_SEND
)
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)

USERNAME_PATTERN = re.compile(r'^@?[a-zA-Z0-9_]{1,32}$')

@router.message(F.text == MENU_BUTTON_SEND)
async def start_send_valentine(message: Message, state: FSMContext, session: AsyncSession):
    try:
        balance_service = BalanceService(session)
        balance = await balance_service.get_balance(message.from_user.id)
        
        if balance < VALENTINE_COST:
            await message.answer(
                text=ERROR_INSUFFICIENT_BALANCE.format(balance=balance),
                reply_markup=get_main_menu()
            )
            return
        
        await state.set_state(SendValentineStates.recipient_username)
        await message.answer(
            text=SEND_VALENTINE_START,
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Помилка в start_send_valentine: {e}")
        await message.answer(text=ERROR_GENERIC)

@router.message(SendValentineStates.recipient_username)
async def process_recipient_username(message: Message, state: FSMContext):
    try:
        username = message.text.strip()
        
        if not USERNAME_PATTERN.match(username):
            await message.answer(text=ERROR_INVALID_USERNAME)
            return
        
        normalized_username = username.lower().lstrip('@')
        sender_username = message.from_user.username
        
        if sender_username and normalized_username == sender_username.lower():
            await message.answer(text=ERROR_SELF_SEND)
            return
        
        await state.update_data(recipient_username=normalized_username)
        await state.set_state(SendValentineStates.message_text)
        
        await message.answer(text=SEND_VALENTINE_MESSAGE)
    except Exception as e:
        logger.error(f"Помилка в process_recipient_username: {e}")
        await message.answer(text=ERROR_GENERIC)

@router.message(SendValentineStates.message_text)
async def process_message_text(message: Message, state: FSMContext):
    try:
        text = message.text.strip()
        
        if len(text) > MAX_VALENTINE_TEXT_LENGTH:
            await message.answer(text=ERROR_MESSAGE_TOO_LONG)
            return
        
        if len(text) == 0:
            await message.answer(text=ERROR_MESSAGE_TOO_LONG)
            return
        
        await state.update_data(message_text=text)
        await state.set_state(SendValentineStates.delivery_slot)
        
        await message.answer(
            text=SEND_VALENTINE_SLOT,
            reply_markup=get_delivery_slot_keyboard()
        )
    except Exception as e:
        logger.error(f"Помилка в process_message_text: {e}")
        await message.answer(text=ERROR_GENERIC)

@router.callback_query(SendValentineStates.delivery_slot, F.data.startswith("slot:"))
async def process_delivery_slot(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    try:
        await callback.answer()
        
        slot = callback.data.split(":")[1]
        
        data = await state.get_data()
        recipient_username = data.get('recipient_username')
        message_text = data.get('message_text')
        
        if not recipient_username or not message_text:
            await callback.message.answer(text=ERROR_GENERIC, reply_markup=get_main_menu())
            await state.clear()
            return
        
        sender_id = callback.from_user.id
        
        balance_service = BalanceService(session)
        balance = await balance_service.get_balance(sender_id)
        
        if balance < VALENTINE_COST:
            await callback.message.answer(
                text=ERROR_INSUFFICIENT_BALANCE.format(balance=balance),
                reply_markup=get_main_menu()
            )
            await state.clear()
            return
        
        valentine_service = ValentineService(session)
        await valentine_service.create_valentine(
            sender_id=sender_id,
            recipient_username=recipient_username,
            message_text=message_text,
            delivery_slot=slot
        )
        
        success = await balance_service.add_balance(sender_id, -VALENTINE_COST)
        
        if not success:
            await callback.message.answer(text=ERROR_GENERIC, reply_markup=get_main_menu())
            await state.clear()
            return
        
        new_balance = await balance_service.get_balance(sender_id)
        
        slot_times = {
            "morning": "10:00",
            "afternoon": "14:00",
            "evening": "20:00"
        }
        
        await callback.message.answer(
            text=VALENTINE_CREATED.format(
                time=slot_times.get(slot, "00:00"),
                balance=new_balance
            ),
            reply_markup=get_main_menu()
        )
        
        await state.clear()
        
        logger.info(f"Створено валентинку від {sender_id} до @{recipient_username}")
        
    except Exception as e:
        logger.error(f"Помилка в process_delivery_slot: {e}")
        await callback.message.answer(text=ERROR_GENERIC, reply_markup=get_main_menu())
        await state.clear()