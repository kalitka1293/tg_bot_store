from pydantic import BaseModel


class TelegramId(BaseModel):
    telegram_id: int
