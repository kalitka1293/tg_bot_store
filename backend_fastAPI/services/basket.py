from models.basket import Basket
from sqlalchemy.ext.asyncio import AsyncSession
from dto import basket
from sqlalchemy.future import select

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from rabbitmq_common_code.producer import ProducerRabbit  # Правильный абсолютный импорт
from rabbitmq_common_code.config_common import BASKET_QUEUE

producer_rabbit = ProducerRabbit(BASKET_QUEUE, 'basket')

async def create_basket(data: basket.Basket, db: AsyncSession):
    baskets = Basket(
        user=data.user,
        quantity=1,
        product_id=data.product_id
    )
    try:
        db.add(baskets)
        await db.commit()
        producer_rabbit.producer(data.get_json('create'))
    except Exception as f:
        print(f)
    return data.user

async def update_basket(data: basket.Basket, db: AsyncSession):
    result = await db.execute(select(Basket).where((Basket.user==data.user) & (Basket.product_id==data.product_id)))
    user = result.scalars().first()
    if user is None:
        await create_basket(data, db)
        return
    user.quantity += data.quantity
    if user.quantity == 0:
        await db.delete(user)
        await db.commit()
        producer_rabbit.producer(data.get_json('delete'))
        return 'Delete product from basket'
    db.add(user)
    await db.commit()
    producer_rabbit.producer(data.get_json('update'))
    return data.user

async def delete_basket(data: basket.Basket, db: AsyncSession):
    result = await db.execute(select(Basket).where(Basket.user == data.user and Basket.product_id == data.product_id))
    user = result.scalars().first()
    await db.delete(user)
    await db.commit()
    producer_rabbit.producer(data.get_json('delete'))
    return data.user


