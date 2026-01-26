# main.py
import asyncio
import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.settings import settings
from bot.dispatcher import create_dispatcher
from database.engine import init_db, close_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    try:
        await init_db()
        logger.info("База даних ініціалізована")
    except Exception as e:
        logger.error(f"Помилка ініціалізації БД: {e}")
        return
    
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = create_dispatcher()
    
    logger.info("Бот запущено")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Помилка під час polling: {e}")
    finally:
        await bot.session.close()
        await close_db()
        logger.info("Бот зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")