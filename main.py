import asyncio
import logging
from aiogram import Dispatcher, Bot
from config.bot_config import bot_config
from routers.handlers.about import about
from utils.logger import get_logger
from routers import commands
from routers.handlers import about, grafmaking, history, clean

logger = get_logger

async def main():
    dp = Dispatcher()
    bot = Bot(token = bot_config.telegram_api_key)

    dp.include_router(commands.router)
    dp.include_router(about.router)
    dp.include_router(grafmaking.router)
    dp.include_router(history.router)
    dp.include_router(clean.router)

    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())