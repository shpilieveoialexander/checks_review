from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveFloat, PositiveInt, validator

from db import constants


class ProductCreate(BaseModel):
    name: str
    price: PositiveFloat
    quantity: PositiveInt


class ReceiptCreate(BaseModel):
    product: List[ProductCreate]
    type: constants.PaymentType
    amount: PositiveFloat

    @validator("amount")
    def validate_amount(cls, value, values):
        total_price = sum(
            product.price * product.quantity for product in values["product"]
        )
        if value < total_price:
            raise ValueError(
                "Amount must be greater than or equal to the total price of product"
            )
        return value


class Product(BaseModel):
    name: str
    price: PositiveFloat


class Position(BaseModel):
    product: Product
    quantity: PositiveInt
    total_price: PositiveFloat


class Receipt(BaseModel):
    id: PositiveInt
    positions: List[Position]
    type: constants.PaymentType
    total: PositiveFloat
    rest: PositiveFloat
    created_at: datetime
