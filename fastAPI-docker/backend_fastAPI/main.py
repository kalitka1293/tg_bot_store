import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import basket as BasketRouter
from routers import product_search as ProductRouter
# from fastapi.responses import JSONResponse
# from fastapi_csrf_protect import CsrfProtect
# from pydantic import BaseModel

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

app.include_router(BasketRouter.router, prefix='/basket')
app.include_router(ProductRouter.router_product_search, prefix='/products')

if __name__ == '__main__':
    uvicorn.run('main:app', log_level="debug")
