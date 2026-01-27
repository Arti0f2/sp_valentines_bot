import sys  #Додано для перевірки платформи
import asyncio
import logging
import signal
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.settings import settings
from bot.dispatcher import create_dispatcher
from database.engine import init_db
from utils.logger import setup_logger

logger = setup_logger(__name__)

shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    logger.info(f"Отримано сигнал {signum}, зупинка бота...")
    
    loop = asyncio.get_running_loop()
    loop.call_soon_threadsafe(shutdown_event.set)

async def main():
   
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, shutdown_event.set)
        loop.add_signal_handler(signal.SIGTERM, shutdown_event.set)
    
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
        
        polling_task = asyncio.create_task(
            dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        )
        
        
        await shutdown_event.wait()
        
        
        logger.info("Зупинка polling...")
        polling_task.cancel()
        
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info("Polling успішно зупинено")
        
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
    finally:
        await bot.session.close()
        logger.info("Сесію бота закрито")

if __name__ == "__main__":
    #КРИТИЧНО ВАЖЛИВИЙ БЛОК ДЛЯ WINDOWS ( для локального тесту )
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #КРИТИЧНО ВАЖЛИВИЙ БЛОК ДЛЯ WINDOWS
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Цей блок ловить Ctrl+C на Windows до того, як event loop запустився або після його закриття
        logger.info("Бот зупинено користувачем (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Неочікувана помилка: {e}")