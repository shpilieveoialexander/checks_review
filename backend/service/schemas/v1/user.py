from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt


class User(BaseModel):
    """Base User fields"""

    id: PositiveInt
    email: EmailStr
    name: Optional[str]
