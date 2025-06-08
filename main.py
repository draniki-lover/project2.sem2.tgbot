import asyncio
import logging
from aiogram import Dispatcher, Bot
from config.bot_config import bot_config
from routers.handlers.about import about
from utils.logger import get_logger
from routers import commands
from routers.handlers import about, grafmaking, history, clean

logger = get_logger(__name__)

async def main():
    logger.info("Starting bot initialization...")

    try:
        dp = Dispatcher()
        bot = Bot(token=bot_config.telegram_api_key)

        dp.include_router(commands.router)
        dp.include_router(about.router)
        dp.include_router(grafmaking.router)
        dp.include_router(history.router)
        dp.include_router(clean.router)

        logger.info("Bot is running...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
