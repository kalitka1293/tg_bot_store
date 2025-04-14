from models.basket import Basket
from sqlalchemy.ext.asyncio import AsyncSession
from dto import basket
from sqlalchemy.future import select

async def create_basket(data: basket.Basket, db: AsyncSession):
    baskets = Basket(
        user=data.user,
        quantity=1,
        product_id=data.product_id
    )
    try:
        db.add(baskets)
        await db.commit()
    except Exception as f:
        print(f)
    return data.user

async def update_basket(data: basket.Basket, db: AsyncSession):
    result = await db.execute(select(Basket).where(Basket.user==data.user and Basket.product_id==data.product_id))
    user = result.scalars().first()
    if user is None:
        return
    user.quantity += data.quantity
    if user.quantity == 0:
        await db.delete(user)
        await db.commit()
        return 'Delete product from basket'
    db.add(user)
    await db.commit()
    return data.user

async def delete_basket(data: basket.Basket, db: AsyncSession):
    result = await db.execute(select(Basket).where(Basket.user == data.user and Basket.product_id == data.product_id))
    user = result.scalars().first()
    await db.delete(user)
    await db.commit()
    return data.user


