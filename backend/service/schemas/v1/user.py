from typing import Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, conint

from db import constants


class User(BaseModel):
    """Base User fields"""

    id: PositiveInt
    email: EmailStr
    name: Optional[str]
