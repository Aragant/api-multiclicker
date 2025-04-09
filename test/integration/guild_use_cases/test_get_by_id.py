import pytest
from domain.guild.use_cases.get_by_id import get_by_id
from domain.guild.use_cases.create import create
from domain.guild.guild_schema import GuildCreateRequestBody
from domain.member.member_repository import MemberRepository
from infrastructure.error.error import NotFoundError
from domain.user.user_repository import UserRepository
from domain.user.user_model import User
import uuid

@pytest.mark.asyncio
async def test_get_by_id_success(transaction):
    # Arrange
    user_id = str(uuid.uuid4())
    username = "test-user"
    
    # Create a user first
    user = User(
        id=user_id,
        username=username,
        email=f"{username}@example.com",
        provider="test"
    )
    await UserRepository().save(user)
    
    guild_data = GuildCreateRequestBody(
        name="Test Guild",
        description="A test guild for testing"
    )
    
    # Create a guild
    created_guild = await create(guild_data, user_id)
    
    # Act
    guild = await get_by_id(created_guild.id)
    
    # Assert
    assert guild is not None, "Guild should not be None"
    assert guild.id == created_guild.id, "Guild ID should match"
    assert guild.name == created_guild.name, "Guild name should match"
    assert guild.description == created_guild.description, "Guild description should match"
    assert guild.sum_member == 1, "Guild should have exactly one member (the creator)"
    assert len(guild.members) == 1, "Guild should have exactly one member in the members list"
    assert guild.members[0] == username, "Member username should match"
    
    # Verify member in database
    member = await MemberRepository().get_active_member_by_user_id(user_id)
    assert member is not None, "Member should exist in database"
    assert member["guild_id"] == created_guild.id, "Member should be associated with the correct guild"

@pytest.mark.asyncio
async def test_get_by_id_not_found(transaction):
    # Act & Assert
    with pytest.raises(NotFoundError) as exc_info:
        await get_by_id("non-existent-id")
    
    assert str(exc_info.value) == "Guilde", "Error message should be 'Guilde'" 