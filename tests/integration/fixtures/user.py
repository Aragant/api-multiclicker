import pytest

from domain.user.use_cases.signup import signup
from domain.user.user_schema import UserSignUp

@pytest.fixture
async def fake_user():
    return await signup(
        UserSignUp(
            username="test",
            email="example@example.fr",
            password="TestPassword123!"
    ))
    