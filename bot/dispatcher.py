# bot/dispatcher.py
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.middlewares.database_middleware import DatabaseMiddleware
from bot.middlewares.user_tracking_middleware import UserTrackingMiddleware
from bot.middlewares.admin_check_middleware import AdminCheckMiddleware
from handlers import register_all_routers

def create_dispatcher() -> Dispatcher:
    # memory storage для fsm (в проді потрібна redis)\n    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # мідлвари для db і трекування користувачів
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(UserTrackingMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(UserTrackingMiddleware())
    
    # регіструємо всі хендлери
    main_router = register_all_routers()
    dp.include_router(main_router)
    
    return dp