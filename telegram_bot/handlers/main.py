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

def get_miniapp_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="Открыть Mini App",
            web_app=types.WebAppInfo(url="https://57a7a3c1557025.lhr.life/mini_app/menu")
        )]
    ])


@router.message(Command('start'))
async def start(message: types.Message | CallbackQuery):

    await message.answer(
        "Welcome to my Mini App!",
        reply_markup=get_miniapp_keyboard()
    )