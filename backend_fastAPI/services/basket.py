from dto import basket
from fastapi import status
from fastapi.responses import JSONResponse
from models.basket import Basket
from rabbitmq_common_code.config_common import BASKET_QUEUE
from rabbitmq_common_code.producer import \
    ProducerRabbit  # Правильный абсолютный импорт
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


producer_rabbit = ProducerRabbit(BASKET_QUEUE, 'basket')


async def create_basket(data: basket.Basket, db: AsyncSession, telegram_id: int):
    baskets = Basket(
        user=telegram_id,
        quantity=1,
        product_id=data.product_id
    )
    try:
        db.add(baskets)
        await db.commit()
        # producer_rabbit.producer(data.get_json('create'))
    except Exception as f:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "Database Error"
            }
        )


async def update_basket(data: basket.Basket, db: AsyncSession, telegram_id: int):
    try:
        result = await db.execute(select(Basket)
                                  .where(
                                    (Basket.user == telegram_id) & (Basket.product_id == data.product_id))
                                        )
        user = result.scalars().first()
        if user is None:
            await create_basket(data, db, telegram_id)
            return
        user.quantity += data.quantity
        if user.quantity == 0:
            await db.delete(user)
            await db.commit()
            producer_rabbit.producer(data.get_json('delete'))
            return status.HTTP_200_OK
        db.add(user)
        await db.commit()
        # try:
        #     producer_rabbit.producer(data.get_json('update'))
        # except Exception as f:
        #     return JSONResponse(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content={
        #             "type": "Producer Error"
        #         }
        #     )
        return status.HTTP_200_OK
    except Exception as f:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "Database Error"
            }
        )


async def delete_basket(data: basket.Basket, db: AsyncSession, telegram_id: int):
    try:
        result = await db.execute(select(Basket).where(Basket.user == telegram_id and Basket.product_id == data.product_id))
        user = result.scalars().first()
        await db.delete(user)
        await db.commit()
        # producer_rabbit.producer(data.get_json('delete'))
        return status.HTTP_200_OK
    except Exception as f:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "Database Error"
            }
        )
