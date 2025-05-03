from utils.setting import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.dispatcher.dispatcher import MemoryStorage

bot_properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    link_preview_is_disabled=False
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(settings.BOT_TOKEN, default=bot_properties)