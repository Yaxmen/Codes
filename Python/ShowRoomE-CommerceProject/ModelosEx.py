from typing import List
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Text,
    Float,
    Date,
    Boolean,
)
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from ConexãoBDEx import Base
from Hash import get_rand_hash

class User(Base):
    __tablename__ = 'Tb_user'
 
    pk_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(Text)
    email = Column(String(50))
    cep = Column(String(10))
    city = Column(String(25))
    address = Column(String(30))
    neighborhood = Column(String(30))
    cellphone = Column(String(25))
    user_token = Column(String(16))
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_employee = Column(Boolean, nullable=False, default=False)
    fk_cart: Mapped["Cart"] = relationship(back_populates="user")


class Product(Base):
    __tablename__ = "Tb_product"

    pk_product = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)
    value = Column(Float)
    stock = Column(Integer)
    product_profile_file = Column(Text, default=None)
    fk_cart: Mapped[List["Cart"]] = relationship()
    fk_product_file: Mapped[List["ProductFile"]] = relationship()


class ProductFile(Base):
    __tablename__ = "Tb_product_file"

    pk_product_file = Column(Integer, primary_key=True, autoincrement=True)
    fk_product: Mapped[str] = mapped_column(ForeignKey("Tb_product.pk_product"))
    file_code = Column(Text)


class Cart(Base):
    __tablename__ = "Tb_cart"

    pk_cart = Column(Integer, primary_key=True, autoincrement=True)
    fk_user: Mapped[str] = mapped_column(ForeignKey("Tb_user.pk_user"))
    user: Mapped["User"] = relationship(back_populates="fk_cart")
    fk_product: Mapped[List["Product"]] = mapped_column(
        ForeignKey("Tb_product.pk_product")
    )
    quantity = Column(Float)


class Authentication(Base):
    __tablename__ = "Tb_authentication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_user: Mapped[str] = mapped_column(ForeignKey("Tb_user.pk_user"))
    access_token = Column(Text)
    expiration = Column(DateTime)


class Order(Base):
    __tablename__ = "Tb_order"

    pk_order = Column(Integer, primary_key=True, autoincrement=True)
    fk_user: Mapped[str] = mapped_column(ForeignKey("Tb_user.pk_user"))
    fk_payment: Mapped[str] = mapped_column(ForeignKey("Tb_payment.pk_payment"))
    fk_delivery_type: Mapped[str] = mapped_column(
        ForeignKey("Tb_delivery_type.pk_delivery")
    )
    order_number = Column(Integer)


association_table = Table(
    "Tb_order_product",
    Base.metadata,
    Column("pk_order_product", Integer, primary_key=True, autoincrement=True),
    Column("fk_order", ForeignKey("Tb_order.pk_order")),
    Column("fk_product", ForeignKey("Tb_product.pk_product")),
    Column("quantity", Integer),
    Column("total_value", Float),
)


class Payment(Base):
    __tablename__ = "Tb_payment"

    pk_payment = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(50))
    address = Column(Text)
    neighborhood = Column(String(30))
    country = Column(String(30))
    value = Column(Float)
    card_name = Column(Text)
    card_number = Column(String(30))
    data_expiration = Column(DateTime)
    fk_order: Mapped["Order"] = relationship()
    fk_payment_type: Mapped[str] = mapped_column(
        ForeignKey("Tb_payment_type.pk_payment_type")
    )


class DeliveryType(Base):
    __tablename__ = "Tb_delivery_type"

    pk_delivery = Column(Integer, primary_key=True, autoincrement=True)
    fk_order: Mapped["Order"] = relationship()
    name = Column(String(50))
    description = Column(Text)


class PaymentType(Base):
    __tablename__ = "Tb_payment_type"

    pk_payment_type = Column(Integer, primary_key=True, autoincrement=True)
    fk_payment: Mapped["Payment"] = relationship()
    name = Column(String(50))
    description = Column(Text)
    type = Column(String(50))