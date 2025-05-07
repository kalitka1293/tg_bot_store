from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

from services import basket as BasketServices
from dto import basket as BasketDTO

router = APIRouter()

@router.post('/', tags=['create_basket'])
async def create(data: BasketDTO.Basket, db: AsyncSession = Depends(get_db)):
    print(data)
    return await BasketServices.create_basket(data, db)

@router.put('/', tags=['update_basket'])
async def update(data: BasketDTO.Basket, db: AsyncSession = Depends(get_db)):
    await BasketServices.update_basket(data, db)
    return {"status": "OK"}
@router.delete('/', tags=['delete_basket'])
async def delete(data: BasketDTO.Basket, db: AsyncSession = Depends(get_db)):
    return await BasketServices.delete_basket(data, db)
