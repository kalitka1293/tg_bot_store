from app import bot, dp
from utils.setting import Settings

async def send_message_channel(text_message:str):
    await bot.send_message(chat_id=Settings.CHANNEL_ID, text=str(text_message))