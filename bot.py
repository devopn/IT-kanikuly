from aiogram import Bot, Dispatcher, types
from db.base import get_session
from db.models import *
import db.service
import logging
import configparser
import asyncio
from config import config

# Import routers
from handlers.command_handler import router as command_router
from handlers.profile_handler import router as profile_router
from handlers.menu_handler import router as menu_router
from handlers.registration_handler import router as registration_router
from handlers.questions_handler import router as questions_router
from handlers.leader_handler import router as leader_router
from handlers.inventory_handler import router as inventory_router
from handlers.friends_handler import router as friends_router
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
        commands=[
            types.BotCommand(command="start", description="Запуск бота"),
            types.BotCommand(command="menu", description="Меню"),
            ]
    )
    

    dp = Dispatcher()
    dp.include_routers(command_router, profile_router, menu_router, registration_router, questions_router, leader_router, inventory_router, friends_router)
    # @dp.callback_query()
    # async def unh_callback(callback: types.CallbackQuery):
    #     await callback.answer("In development")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())