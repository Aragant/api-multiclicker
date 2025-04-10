from sqlite3 import IntegrityError
import pytest
import pytest_asyncio
from infrastructure.database.base_repository import BaseRepository
from fake_model import FakeModel
@pytest_asyncio.fixture(scope="function")
async def repo(transaction):
    return BaseRepository(FakeModel, lambda: transaction)

@pytest.mark.asyncio
async def test_create_when_the_data_is_valid_should_return_it(repo):
    """Teste la création d'un élément dans la base de données."""
    result = await repo._save(FakeModel(username="test"))
    assert result.get("username") == "test"
    
    
@pytest.mark.asyncio
async def test_create_when_the_data_is_not_valid_should_return(repo):
    with pytest.raises(Exception):
        await repo._save(FakeModel(username=None))
