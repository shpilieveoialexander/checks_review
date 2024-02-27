from enum import Enum


class PaymentType(str, Enum):
    """Payment type"""

    CASH = "CASH"
    CASHLESS = "CASHLESS"
