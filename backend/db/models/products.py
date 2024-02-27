from sqlalchemy import (VARCHAR, CheckConstraint, Column, ForeignKey, Integer,
                        Numeric, String)
from sqlalchemy.orm import relationship

from db import constants

from .base import BaseModel


class Product(BaseModel):
    name = Column(String(length=40), doc="Products name")
    price = Column(Numeric(precision=10, scale=2), doc="Product price")


class Position(BaseModel):
    product_id = Column(
        Integer,
        ForeignKey("product.id", ondelete="CASCADE"),
        doc="Product id",
    )
    quantity = Column(
        Integer,
        CheckConstraint("quantity > 0"),
        nullable=False,
        doc="Quantity of Products",
    )
    total_price = Column(Numeric(precision=10, scale=2), doc="Total price")
    receipt_id = Column(
        Integer,
        ForeignKey("receipt.id", ondelete="CASCADE"),
        doc="Receipt id",
    )
    product = relationship("Product", lazy="subquery")


class Receipt(BaseModel):
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        doc="User id",
    )

    type = Column(
        VARCHAR,
        nullable=False,
        default=constants.PaymentType.CASH.value,
        doc="Type of Payment",
    )
    rest = Column(Numeric(precision=10, scale=2), doc="Receipt rest")
    total = Column(Numeric(precision=10, scale=2), doc="Receipt amount")

    user = relationship("User", uselist=False, lazy="joined")
    positions = relationship("Position", lazy="subquery")
