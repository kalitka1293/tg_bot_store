from meilisearch import Client

from dotenv import load_dotenv
import os
from pathlib import Path

path_env = Path(os.path.dirname(__file__), '.env')
if os.path.exists(path_env):
    load_dotenv(path_env)
else:
    raise FileExistsError('Нет файла .env')

client = Client(os.getenv('HOST_MEILISEARCH'), api_key=os.getenv('MASTER_KEY_MEILISEARCH'))

