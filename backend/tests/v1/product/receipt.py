import random

from fastapi import status

from tests import factories
from tests.conftests import TestCase
from tests.factories.utils import fake
from tests.utils import get_headers


class CreateReceiptTestCase(TestCase):
    def setUp(self) -> None:
        self.url = "/api/v1/receipt/"
        self.user = factories.UserFactory()
        self.data = {
            "product": [
                {
                    "name": fake.name(),
                    "price": random.uniform(10, 30),
                    "quantity": random.randint(0, 10),
                }
            ],
            "type": "CASH",
            "amount": random.randint(1000, 2000),
        }

    def test_create_product(self) -> None:
        response = self.client.post(
            self.url, json=self.data, headers=get_headers(self.user.id)
        )
        response.json()
        assert response.status_code == status.HTTP_201_CREATED
