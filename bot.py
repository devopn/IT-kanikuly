from aiogram import Bot, Dispatcher, types
from db.base import get_session
from db.models import *
import db.service
import logging
import configparser
import asyncio
from config import config

from handlers.command_handler import router as command_router
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
async def main():

    # Set up bot
    bot = Bot(config.tg_api)
    await bot.set_my_commands(
        commands=[types.BotCommand(command="start", description="Запуск бота")]
    )


    dp = Dispatcher()
    dp.include_routers(command_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())