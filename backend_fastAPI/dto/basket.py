from pydantic import BaseModel

class Basket(BaseModel):
    product_id: int
    user: int
    quantity: int
