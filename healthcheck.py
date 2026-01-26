# healthcheck.py
import asyncio
from aiohttp import web
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def health(request):
    return web.Response(text='OK', status=200)

async def run_healthcheck():
    app = web.Application()
    app.router.add_get('/health', health)
    app.router.add_get('/', health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    logger.info("Healthcheck server запущено на порту 8080")
    
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()
        logger.info("Healthcheck server зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(run_healthcheck())
    except KeyboardInterrupt:
        logger.info("Healthcheck server зупинено користувачем")