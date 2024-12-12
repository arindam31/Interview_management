import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Fixture to return an API client instance.
    """
    return APIClient()


def get_authenticated_client(username: str, password: str):
    """Fixture to get authenticated client with Bearer token."""

    client = APIClient()

    # Obtain the access token from the auth API
    response = client.post(
        "/users/api/token/", {"username": username, "password": password}
    )
    assert response.status_code == status.HTTP_200_OK

    # Get the token and set it in the authorization header
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client
