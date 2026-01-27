from aiogram import Router
from handlers.common import start, help
from handlers.donate import donate
from handlers.admin import manual_topup
from handlers.valentines import router as valentines_router

def register_all_routers() -> Router:
    """
    Ця функція збирає всі "гілки" логіки в один головний роутер.
    """
    main_router = Router()
    
    
    main_router.include_router(manual_topup.router)
    
   
    main_router.include_router(donate.router)
    main_router.include_router(valentines_router)
    

    main_router.include_router(start.router)
    main_router.include_router(help.router)
    
    return main_router

__all__ = ['register_all_routers']