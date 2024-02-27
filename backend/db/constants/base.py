from enum import Enum


class BaseChoices(int, Enum):
    """Permission type"""

    def __new__(cls, value, label="..."):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj
