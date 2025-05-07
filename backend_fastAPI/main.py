import uvicorn
from fastapi import FastAPI
from routers import basket as BasketRouter
from routers import product_search as ProductRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Настройка безопастности требуется
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ec6210a713515c.lhr.life",  # Ваш фронтенд
        "http://localhost:3000"             # Для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],                    # Явно укажите PUT, DELETE если нужно
    allow_headers=["*"],
    expose_headers=["X-Custom-Header"],     # Если используются кастомные заголовки
    max_age=600
)

app.include_router(BasketRouter.router, prefix='/basket')
app.include_router(ProductRouter.router_product_search, prefix='/products')

if __name__ == '__main__':
    uvicorn.run('main:app')