from pydantic import BaseModel


class Basket(BaseModel):
    product_id: int
    quantity: int

    def get_json(self, action):
        """
        :param action: ['create', 'update', 'delete']
        :return: dict
        """
        return {
            "product_id": self.product_id,
            "user": self.user,
            "quantity": self.quantity,
            "action": action
        }
