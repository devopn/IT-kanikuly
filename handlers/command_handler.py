from aiogram import types, Router
from aiogram.filters import Command
router = Router()
from yandex_api import get_text 


# @router.message(Command("start"))
# async def start_command(message: types.Message):
    

@router.message()
async def echo(message: types.Message):
    await message.answer("Начал работу")
    text = await get_text(message.text, 0.7, limit=1000)
    
    await message.answer(text)