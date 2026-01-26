# bot/filters/registration_filter.py
from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService

class IsRegisteredFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user_service = UserService(session)
        return await user_service.is_registered(message.from_user.id)