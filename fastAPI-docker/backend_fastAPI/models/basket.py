from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Basket(Base):
    __tablename__ = 'order_basket'

    id: Mapped[int] = mapped_column(
                                    primary_key=True, autoincrement=True,
                                    unique=True, nullable=True
                                    )
    user: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
