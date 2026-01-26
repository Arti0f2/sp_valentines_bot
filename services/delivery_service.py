# services/delivery_service.py
import logging
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from services.valentine_service import ValentineService
from services.user_service import UserService
from services.notification_service import NotificationService
from localization.texts import VALENTINE_RECEIVED, VALENTINE_NOT_DELIVERED
from utils.logger import get_logger

logger = get_logger(__name__)

class DeliveryService:
    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.valentine_service = ValentineService(session)
        self.user_service = UserService(session)
        self.notification_service = NotificationService(bot)
    
    async def deliver_valentines_for_slot(self, delivery_slot: str) -> tuple[int, int]:
        try:
            valentines = await self.valentine_service.get_pending_for_delivery(delivery_slot)
            
            delivered = 0
            failed = 0
            
            for valentine in valentines:
                try:
                    success = await self.deliver_valentine(valentine)
                    if success:
                        delivered += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Помилка доставки валентинки #{valentine.id}: {e}")
                    failed += 1
            
            logger.info(f"Доставлено: {delivered}, Не доставлено: {failed} для слоту {delivery_slot}")
            
            return delivered, failed
        except Exception as e:
            logger.error(f"Критична помилка в deliver_valentines_for_slot: {e}")
            return 0, 0
    
    async def deliver_valentine(self, valentine) -> bool:
        try:
            recipient = await self.user_service.get_user_by_username(valentine.recipient_username)
            
            if recipient is None:
                await self.valentine_service.mark_failed(valentine.id)
                
                sender = await self.user_service.get_user(valentine.sender_id)
                if sender:
                    await self.notification_service.send_message(
                        user_id=sender.user_id,
                        text=VALENTINE_NOT_DELIVERED.format(username=valentine.recipient_username)
                    )
                
                logger.warning(f"Одержувача @{valentine.recipient_username} не знайдено")
                return False
            
            text = VALENTINE_RECEIVED.format(text=valentine.message_text)
            
            success = await self.notification_service.send_message(
                user_id=recipient.user_id,
                text=text
            )
            
            if success:
                await self.valentine_service.mark_sent(valentine.id)
                logger.info(f"Валентинку #{valentine.id} доставлено до {recipient.user_id}")
                return True
            else:
                await self.valentine_service.mark_failed(valentine.id)
                logger.error(f"Не вдалося доставити валентинку #{valentine.id}")
                return False
        except Exception as e:
            logger.error(f"Помилка в deliver_valentine для #{valentine.id}: {e}")
            try:
                await self.valentine_service.mark_failed(valentine.id)
            except:
                pass
            return False