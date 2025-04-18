from sqlalchemy.orm import (sessionmaker, DeclarativeBase, Session,
                            Mapped, mapped_column, relationship)
from sqlalchemy.engine import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import joinedload

engine = create_engine("postgresql+psycopg2://tg:tg@localhost:5432/tg_store")

session = sessionmaker(
    engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=True,
)

class Base(DeclarativeBase):
    pass

def get_db() -> Session:
    with session() as s:
        return s

class Country(Base):
    __tablename__ = "mini_app_country"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<Country(id={self.id}, country={self.country!r})>"

class SubcategoryProduct(Base):
    __tablename__ = "mini_app_subcategoryproduct"

    id: Mapped[int] = mapped_column(primary_key=True)
    subcategory_product: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<SubcategoryProduct(id={self.id}, subcategory={self.subcategory_product!r})>"

class TypeEquipment(Base):
    __tablename__ = "mini_app_typeequipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_equipment: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<TypeEquipment(id={self.id}, type={self.type_equipment!r})>"

class Brand(Base):
    __tablename__ = "mini_app_brand"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<Brand(id={self.id}, brand={self.brand!r})>"

class Product(Base):
    __tablename__ = "mini_app_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

    brand_id: Mapped[int] = mapped_column(ForeignKey("mini_app_brand.id"))
    country_id: Mapped[int] = mapped_column(ForeignKey("mini_app_country.id"))
    group_product_id: Mapped[int] = mapped_column(ForeignKey("mini_app_subcategoryproduct.id"))
    type_equipment_id: Mapped[int] = mapped_column(ForeignKey("mini_app_typeequipment.id"))

    brand: Mapped["Brand"] = relationship()
    country: Mapped["Country"] = relationship()
    group_product: Mapped["SubcategoryProduct"] = relationship()
    type_equipment: Mapped["TypeEquipment"] = relationship()
    parameters: Mapped[list["ParameterProduct"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name!r})>"

class ParameterProduct(Base):
    __tablename__ = "mini_app_parameterproduct"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column()
    value: Mapped[str] = mapped_column()

    product_id: Mapped[int] = mapped_column(ForeignKey("mini_app_product.id", ondelete="CASCADE"))
    product: Mapped["Product"] = relationship(back_populates="parameters")

    def __repr__(self):
        return f"<ParameterProduct(id={self.id}, key={self.key!r})>"


def get_product_data_meilisearch(product_id: int) -> dict:
    import time
    time.sleep(0.2)
    print(product_id, type(product_id))
    db = get_db()
    result = (
        db.query(Product)
        .options(
            joinedload(Product.country),
            joinedload(Product.brand),
            joinedload(Product.group_product),
            joinedload(Product.type_equipment)
        )
        .where(Product.id == product_id)
        .first()
    )
    print(result)
    data = {
        "id": result.id,
        "name": result.name,
        "description": result.description,
        "price": result.price,
        "brand": result.brand.brand,
        "country": result.country.country,
        "group_product": result.group_product.subcategory_product,
        "type_equipment": result.type_equipment.type_equipment
    }
    db.close()
    return data

def get_all_product_data_meilisearch() -> list:
    db = get_db()
    scl = (
        db.query(Product)
        .options(
            joinedload(Product.country),
            joinedload(Product.brand),
            joinedload(Product.group_product),
            joinedload(Product.type_equipment)
        )
    )
    db.close()
    list_data = []
    for result in scl.all():
        list_data.append({
        "id": result.id,
        "name": result.name,
        "description": result.description,
        "price": result.price,
        "brand": result.brand.brand,
        "country": result.country.country,
        "group_product": result.group_product.subcategory_product,
        "type_equipment": result.type_equipment.type_equipment
    })
    return list_data
