from dotenv import load_dotenv
import os
from pathlib import Path

path_env = Path(os.path.dirname(__file__), '.env')
if os.path.exists(path_env):
    load_dotenv(path_env)
else:
    raise FileExistsError('Нет файла .env')

LIST_NOT_USE_VAR = ['path_env']

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
