from typing import Annotated

from database import get_db
from dto import basket as BasketDTO
from dto.token_jwt import TelegramId
from fastapi import APIRouter, Depends, Request
from services import basket as BasketServices
from services.token_jwt import validation_authorization_get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()


@router.post('/', tags=['create_basket'])
async def create(
    data: BasketDTO.Basket,
    telegram_id: Annotated[
        TelegramId,
        Depends(validation_authorization_get_current_user)
    ],
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    await csrf_protect.validate_csrf(request)
    return await BasketServices.create_basket(data, db, telegram_id.telegram_id)


@router.put('/', tags=['update_basket'])
async def update(data: BasketDTO.Basket,
                 telegram_id: Annotated[
                     TelegramId,
                     Depends(validation_authorization_get_current_user)
                 ],
                 db: AsyncSession=Depends(get_db)):
    return await BasketServices.update_basket(data, db, telegram_id.telegram_id)


@router.delete('/', tags=['delete_basket'])
async def delete(data: BasketDTO.Basket,
                 telegram_id: Annotated[
                     TelegramId,
                     Depends(validation_authorization_get_current_user)
                 ],
                 db: AsyncSession=Depends(get_db)):
    return await BasketServices.delete_basket(data, db, telegram_id.telegram_id)
