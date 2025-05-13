import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import basket as BasketRouter
from routers import product_search as ProductRouter

app = FastAPI()
# Настройка безопастности требуется
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cca2208ee22e0c.lhr.life",
        "http://127.0.0.1:8080",
        "127.0.0.1:8080",
        "127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

app.include_router(BasketRouter.router, prefix='/basket')
app.include_router(ProductRouter.router_product_search, prefix='/products')

if __name__ == '__main__':
    uvicorn.run('main:app')
