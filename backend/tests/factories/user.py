import random

from factory import Faker, LazyFunction, SubFactory

from db import constants, models

from .base import BaseFactory
from .utils import fake


class UserFactory(BaseFactory):
    email = LazyFunction(lambda: f"{random.randint(1, 999)}{fake.email()}")
    password = LazyFunction(lambda: fake.password())
    name = Faker("name")


    class Meta:
        model = models.User

