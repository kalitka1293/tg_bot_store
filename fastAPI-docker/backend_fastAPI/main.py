import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import basket as BasketRouter
from routers import product_search as ProductRouter
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect, CsrfProtectError
from pydantic import BaseSettings

app = FastAPI(root_path="/api")
# Настройка безопастности требуется
origin = [
    "https://shovik.ru",
    "https://www.shovik.ru",
    "http://127.0.0.1:8000",
    "localhost"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

import os
from pathlib import Path
from dotenv import load_dotenv

path_env = Path(os.path.dirname(__file__), '.env')
if os.path.exists(path_env):
    load_dotenv(path_env)
else:
    raise FileExistsError('Нет файла .env')

class CsrfSettings(BaseSettings):
    secret_key: str = str(os.getenv("CSRF_SECRET_KEY"))

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.get("/csrf-token/")
def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    response = JSONResponse(content={"detail": "CSRF cookie set"})
    csrf_protect.set_csrf_cookie(response)
    return response

app.include_router(BasketRouter.router, prefix='/basket')
app.include_router(ProductRouter.router_product_search, prefix='/products')

if __name__ == '__main__':
    uvicorn.run('main:app')
