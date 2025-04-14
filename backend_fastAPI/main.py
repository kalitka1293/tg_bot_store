import uvicorn
from fastapi import FastAPI
from routers import basket as BasketRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(BasketRouter.router, prefix='/basket')

if __name__ == '__main__':
    uvicorn.run('main:app')