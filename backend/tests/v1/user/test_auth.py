import random

from fastapi import status

from service.core.security import hash_password
from tests import factories
from tests.conftests import TestCase
from tests.factories.utils import fake
from tests.utils import get_refresh_headers


class LoginTestCase(TestCase):
    def setUp(self) -> None:
        self.url = "/api/v1/auth/access-token"
        self.data = {
            "email": f"{random.randint(1, 999)}{fake.email()}",
            "password": fake.password(),
        }

    def test_success_login(self) -> None:
        factories.UserFactory(
            email=self.data["email"], password=hash_password(self.data["password"])
        )
        response = self.client.post(self.url, data=self.data)
        resp_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert resp_data["access_token"] is not None
        assert resp_data["refresh_token"] is not None

    def test_fail_login_with_wrong_email(self) -> None:
        factories.UserFactory(
            email=fake.email(), password=hash_password(fake.password())
        )
        response = self.client.post(self.url, data=self.data)
        resp_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert resp_data["detail"] == "User blocked or not found"

    def test_fail_login_with_wrong_password(self) -> None:
        factories.UserFactory(
            email=self.data["email"], password=hash_password(fake.password())
        )
        response = self.client.post(self.url, data=self.data)
        resp_data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert resp_data["detail"] == "Invalid credentials"


class SignUpTestCase(TestCase):
    def setUp(self) -> None:
        self.url = "/api/v1/auth/sign-up/"
        password = fake.password()
        self.data = {
            "name": fake.name(),
            "email": f"{random.randint(1, 999)}{fake.email()}",
            "password": password,
            "password_confirm": password,
        }

    def test_success_sign_up(self) -> None:
        response = self.client.post(self.url, data=self.data)
        resp_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert resp_data["access_token"] is not None
        assert resp_data["refresh_token"] is not None

    def test_fail_with_password_missmatch(self) -> None:
        self.data["password_confirm"] = fake.password()
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_fail_with_invalid_email(self) -> None:
        self.data["email"] = fake.name()
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_fail_with_user_email_exists(self) -> None:
        factories.UserFactory(
            email=self.data["email"], password=hash_password(self.data["password"])
        )
        response = self.client.post(self.url, data=self.data)
        resp_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert resp_data["detail"] == f"User with email {self.data['email']} exists"


class RefreshTokenTestCase(TestCase):
    def setUp(self) -> None:
        self.url = "/api/v1/auth/refresh-token/"

    def test_success_refresh_token(self) -> None:
        user = factories.UserFactory()
        response = self.client.post(self.url, headers=get_refresh_headers(user.id))
        resp_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert resp_data["access_token"] is not None
        assert resp_data["refresh_token"] is not None

    def test_fail_refresh_token_with_invalid_user_id(self) -> None:
        response = self.client.post(
            self.url, headers=get_refresh_headers(random.randint(1, 999))
        )
        resp_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert resp_data["detail"] == "User not found"

    def test_fail_with_invalid_refresh_token(self) -> None:
        response = self.client.post(
            self.url, headers={"Authorization": f"Bearer {fake.word()}"}
        )
        resp_data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert resp_data["detail"] == "Could not validate credentials"

    def test_fail_refresh_token_without_headers(self) -> None:
        response = self.client.post(self.url)
        resp_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert resp_data["detail"] == "Not authenticated"
