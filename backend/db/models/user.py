from sqlalchemy import (VARCHAR, Boolean, CheckConstraint, Column, ForeignKey,
                        Integer, String)

from db import constants

from .base import BaseModel


class User(BaseModel):
    """User table"""

    email = Column(String, unique=True, nullable=False, doc="Unique email address")
    password = Column(String, nullable=False, doc="Hashed password")
    name = Column(String(length=40), doc="User name")

    def __repr__(self):
        return f"User: <ID{self.id}:{self.email}>"

    def __str__(self):
        return f"User: <ID{self.id}:{self.email}>"
