from sqlalchemy.orm import Mapped, mapped_column
from database import Base, get_db
from sqlalchemy.dialects.postgresql import INT8RANGE, INT4RANGE, SMALLINT

class Basket(Base):
    __tablename__ = 'mini_app_basket'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=True)
    user: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()