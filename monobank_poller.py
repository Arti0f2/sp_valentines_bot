# monobank_poller.py
import asyncio
import logging
from datetime import datetime
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.settings import settings
from config.constants import MONOBANK_POLL_INTERVAL
from database.engine import async_session_factory, init_db, close_db
from services.monobank_service import MonobankService
from services.balance_service import BalanceService
from services.notification_service import NotificationService
from localization.texts import BALANCE_UPDATED

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def poll_monobank():
    try:
        await init_db()
        logger.info("База даних ініціалізована для Monobank poller")
    except Exception as e:
        logger.error(f"Помилка ініціалізації БД: {e}")
        return
    
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    logger.info("Monobank poller запущено")
    
    try:
        while True:
            try:
                async with async_session_factory() as session:
                    monobank_service = MonobankService(session, settings.MONOBANK_TOKEN)
                    balance_service = BalanceService(session)
                    notification_service = NotificationService(bot)
                    
                    processed = await monobank_service.sync_transactions()
                    
                    for user_id, amount in processed:
                        user_balance = await balance_service.get_balance(user_id)
                        
                        await notification_service.send_message(
                            user_id=user_id,
                            text=BALANCE_UPDATED.format(
                                amount=amount,
                                balance=user_balance
                            )
                        )
                    
                    if processed:
                        logger.info(f"Оброблено транзакцій: {len(processed)}")
                
            except Exception as e:
                logger.error(f"Помилка в циклі polling: {e}")
            
            await asyncio.sleep(MONOBANK_POLL_INTERVAL)
    
    except KeyboardInterrupt:
        logger.info("Monobank poller зупинено користувачем")
    finally:
        await bot.session.close()
        await close_db()
        logger.info("Monobank poller зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(poll_monobank())
    except KeyboardInterrupt:
        logger.info("Monobank poller зупинено користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")