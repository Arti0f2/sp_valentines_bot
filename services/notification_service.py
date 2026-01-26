# services/notification_service.py
from typing import Optional, List
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError, TelegramBadRequest
from utils.logger import get_logger

logger = get_logger(__name__)

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def send_message(self, user_id: int, text: str, reply_markup=None) -> bool:
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=reply_markup
            )
            return True
        except TelegramForbiddenError:
            logger.warning(f"User {user_id} blocked the bot")
            return False
        except TelegramBadRequest as e:
            logger.warning(f"Bad request for user {user_id}: {e}")
            return False
        except TelegramAPIError as e:
            logger.error(f"Telegram API error for user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message to {user_id}: {e}")
            return False
    
    async def send_photo(
        self,
        user_id: int,
        photo,
        caption: Optional[str] = None,
        reply_markup=None
    ) -> bool:
        try:
            await self.bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=caption,
                reply_markup=reply_markup
            )
            return True
        except TelegramForbiddenError:
            logger.warning(f"User {user_id} blocked the bot")
            return False
        except TelegramBadRequest as e:
            logger.warning(f"Bad request for user {user_id}: {e}")
            return False
        except TelegramAPIError as e:
            logger.error(f"Telegram API error for user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending photo to {user_id}: {e}")
            return False
    
    async def notify_admins(
        self,
        admin_ids: List[int],
        text: str,
        photo=None,
        reply_markup=None
    ) -> None:
        for admin_id in admin_ids:
            try:
                if photo:
                    await self.send_photo(admin_id, photo, text, reply_markup)
                else:
                    await self.send_message(admin_id, text, reply_markup)
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
                continue
    
    async def broadcast(self, user_ids: List[int], text: str, reply_markup=None) -> tuple[int, int]:
        success_count = 0
        fail_count = 0
        
        for user_id in user_ids:
            try:
                success = await self.send_message(user_id, text, reply_markup)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                logger.error(f"Broadcast failed for user {user_id}: {e}")
                fail_count += 1
        
        logger.info(f"Broadcast completed: {success_count} success, {fail_count} failed")
        return success_count, fail_count