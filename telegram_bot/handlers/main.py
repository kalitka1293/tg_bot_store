from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from aiogram.types import WebAppInfo,WebAppData
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackQuery
import asyncio
from app import dp, bot
from aiogram.types import WebAppInfo

router = Router()

#pydantic_settings

@router.message(Command('start'))
async def start(message: types.Message | CallbackQuery):
    wb = WebAppInfo(url='https://e3035e97461c6c.lhr.life/mini_app/menu/')

    b = types.KeyboardButton(text='lol', web_app=wb)
    markup = types.ReplyKeyboardMarkup(keyboard=[[b]])

    await message.answer(
        "Welcome to my Mini App!",
        reply_markup=markup
    )

    await message.answer('Ты опять меня запустил?')