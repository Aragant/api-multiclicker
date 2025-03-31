import pytest
import pytest_asyncio
from infrastructure.database.transaction import transaction
from domain.user.user_repository import BaseRepository
from fake_model import FakeModel


@pytest_asyncio.fixture(scope="session")
async def repo(async_session):
    return BaseRepository(FakeModel, lambda: transaction(async_session))


@pytest.mark.asyncio
async def test_get(async_session, repo):
    """Teste la récupération d'un élément dans la base de données."""
    async with async_session as session:
        session.add(FakeModel(id=1, username="test"))
        await session.commit()

    result = await repo._get(id=1)
    assert result.get("id") == 1
    assert result.get("username") == "test"
