from aiogram import Router
from .send_valentine import router as send_valentine_router
router = Router()
router.include_router(send_valentine_router)