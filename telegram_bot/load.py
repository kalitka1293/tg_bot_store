import asyncio
import argparse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from rabbitmq.broker import consumer_tg
from utils.logging_prog import logging_use

from handlers import dp, bot, router

import logging

logging.basicConfig(level=logging.WARNING)

# На сервере узнать timezone. Use timedatectl
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

async def on_startup():
    scheduler.add_job(
        func=consumer_tg,
        trigger='interval',
        seconds=60
    )
    scheduler.start()

def arg():
    parser = argparse.ArgumentParser(description='Вкл/Выкл логирования в журнал')
    parser.add_argument('-log', help='0 - Выкл, 1 - Вкл', type=int, default=0)
    args = parser.parse_args()
    logging_use(args.log)

async def load_dp():
    dp.include_router(router)
    await dp.start_polling(bot)

async def load():
    task1 = asyncio.create_task(load_dp())
    task2 = asyncio.create_task(on_startup())
    await asyncio.gather(*[task1, task2])

if __name__ == '__main__':
    arg()
    asyncio.run(load())