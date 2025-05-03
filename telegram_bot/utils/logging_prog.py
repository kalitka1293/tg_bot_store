import logging
from aiogram.filters.command import CommandException

logging.getLogger('apscheduler').setLevel(logging.WARNING)

def logging_use(write_log: int)-> None:
    if write_log == 1:
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a",
                           format="%(asctime)s||%(levelname)s :%(message)s")
        return
    elif write_log == 0:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s||%(levelname)s :%(message)s")
        return
    else:
        raise CommandException('logging incorrect argument')