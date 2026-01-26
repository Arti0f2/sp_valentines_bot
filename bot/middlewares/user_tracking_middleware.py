# bot/middlewares/user_tracking_middleware.py
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService

class UserTrackingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data.get('session')
        
        if session and isinstance(event, (Message, CallbackQuery)):
            try:
                user_service = UserService(session)
                
                if isinstance(event, Message):
                    user = event.from_user
                elif isinstance(event, CallbackQuery):
                    user = event.from_user
                else:
                    return await handler(event, data)
                
                if user:
                    await user_service.update_username_if_changed(
                        user.id,
                        user.username
                    )
            except Exception:
                pass
        
        return await handler(event, data)