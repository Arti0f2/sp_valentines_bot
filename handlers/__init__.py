# handlers/__init__.py
from aiogram import Router
from handlers.common import start, help
from handlers.donate import donate
from handlers.admin import manual_topup

def register_all_routers() -> Router:
    main_router = Router()
    
    main_router.include_router(start.router)
    main_router.include_router(help.router)
    main_router.include_router(donate.router)
    main_router.include_router(manual_topup.router)
    
    return main_router

__all__ = ['register_all_routers']