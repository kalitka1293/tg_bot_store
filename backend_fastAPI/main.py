import uvicorn
from fastapi import FastAPI
from routers import basket as BasketRouter
from routers import product_search as ProductRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Настройка безопастности требуется
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(BasketRouter.router, prefix='/basket')
app.include_router(ProductRouter.router_product_search, prefix='/products')

if __name__ == '__main__':
    uvicorn.run('main:app')