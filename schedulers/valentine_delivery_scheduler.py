# schedulers/valentine_delivery_scheduler.py
import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.settings import settings
from config.constants import DELIVERY_DATE_DAY, DELIVERY_DATE_MONTH
from database.engine import async_session_factory
from services.delivery_service import DeliveryService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def deliver_morning():
    logger.info("Запуск доставки: ранковий слот")
    await deliver_slot("morning")

async def deliver_afternoon():
    logger.info("Запуск доставки: денний слот")
    await deliver_slot("afternoon")

async def deliver_evening():
    logger.info("Запуск доставки: вечірній слот")
    await deliver_slot("evening")

async def deliver_slot(slot: str):
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    try:
        async with async_session_factory() as session:
            delivery_service = DeliveryService(session, bot)
            delivered, failed = await delivery_service.deliver_valentines_for_slot(slot)
            logger.info(f"Слот {slot}: доставлено {delivered}, не доставлено {failed}")
    except Exception as e:
        logger.error(f"Помилка доставки слоту {slot}: {e}")
    finally:
        await bot.session.close()

async def run_scheduler():
    scheduler = AsyncIOScheduler(timezone=timezone(settings.TIMEZONE))
    
    scheduler.add_job(
        deliver_morning,
        trigger=CronTrigger(
            month=DELIVERY_DATE_MONTH,
            day=DELIVERY_DATE_DAY,
            hour=10,
            minute=0,
            timezone=settings.TIMEZONE
        ),
        id='deliver_morning'
    )
    
    scheduler.add_job(
        deliver_afternoon,
        trigger=CronTrigger(
            month=DELIVERY_DATE_MONTH,
            day=DELIVERY_DATE_DAY,
            hour=14,
            minute=0,
            timezone=settings.TIMEZONE
        ),
        id='deliver_afternoon'
    )
    
    scheduler.add_job(
        deliver_evening,
        trigger=CronTrigger(
            month=DELIVERY_DATE_MONTH,
            day=DELIVERY_DATE_DAY,
            hour=20,
            minute=0,
            timezone=settings.TIMEZONE
        ),
        id='deliver_evening'
    )
    
    scheduler.start()
    logger.info("Scheduler запущено")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        logger.info("Scheduler зупинено користувачем")