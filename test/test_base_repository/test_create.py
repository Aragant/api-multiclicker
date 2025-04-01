import pytest
import pytest_asyncio
from infrastructure.database.transaction import transaction
from infrastructure.database.base_repository import BaseRepository
from fake_model import FakeModel


# @pytest_asyncio.fixture(scope="function")
# async def repo(async_session):
#     return BaseRepository(FakeModel, lambda: transaction(async_session))


# @pytest.mark.asyncio
# async def test_create_when_the_data_is_valid_should_return_it(repo):
#     result = await repo._save(FakeModel(username="test"))
    
#     assert result.get("username") == "test"
    
    
# @pytest.mark.asyncio
# async def test_create_when_the_data_is_not_valid_should_return(repo):
#     result = await repo._save(FakeModel())
    
#     assert result.get("username") == "test"