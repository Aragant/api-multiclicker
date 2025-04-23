import pytest

from tests.integration.fixtures.user import fake_user




@pytest.mark.asyncio
async def test_update_profile_when_success_should_return_user(fake_user: fake_user):
    user = fake_user
    assert user.username == "test"