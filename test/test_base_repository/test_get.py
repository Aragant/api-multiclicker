import pytest
import pytest_asyncio
from infrastructure.database.base_repository import BaseRepository
from fake_model import FakeModel


@pytest_asyncio.fixture(scope="function")
async def repo(transaction):
    return BaseRepository(FakeModel, lambda: transaction)


@pytest.mark.asyncio
async def test_get_when_the_data_exists_should_return_it(async_session, repo):
    """Teste la récupération d'un élément dans la base de données."""
    async with async_session as session:
        session.add(FakeModel(id=1, username="test"))

        result = await repo._get(id=1)
        assert result.get("id") == 1
        assert result.get("username") == "test"
    
    
@pytest.mark.asyncio
async def test_get_when_the_data_does_not_exist_should_return_none(async_session, repo):
    result = await repo._get(id=1)
    assert result is None