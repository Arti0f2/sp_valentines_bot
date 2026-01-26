# handlers/common/start.py
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService
from bot.keyboards.main_menu import get_main_menu
from localization.texts import WELCOME_MESSAGE, ERROR_GENERIC
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    try:
        user_service = UserService(session)
        
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name or "Користувач"
        
        is_registered = await user_service.is_registered(user_id)
        
        if not is_registered:
            await user_service.register_user(
                user_id=user_id,
                username=username,
                full_name=full_name
            )
            logger.info(f"Зареєстровано нового користувача: {user_id}")
        else:
            await user_service.update_username_if_changed(user_id, username)
        
        await message.answer(
            text=WELCOME_MESSAGE.format(name=full_name),
            reply_markup=get_main_menu()
        )
    
    except Exception as e:
        logger.error(f"Помилка в cmd_start для користувача {message.from_user.id}: {e}")
        await message.answer(text=ERROR_GENERIC)