import pytest
from domain.guild.use_cases.create_guild import create_guild
from domain.guild.guild_schema import GuildCreateRequestBody
from infrastructure.error.error import ConflictError, DuplicateEntryError
from domain.member.member_model import MemberRole
from domain.member.member_repository import MemberRepository
from domain.guild.guild_repository import GuildRepository

@pytest.mark.asyncio
async def test_create_success():
    # Arrange
    user_id = "test-user-id"
    guild_data = GuildCreateRequestBody(
        name="Test Guild",
        description="A test guild for testing"
    )
    
    # Act
    guild = await create_guild(guild_data, user_id)
    
    # Assert
    assert guild.name == guild_data.name
    assert guild.description == guild_data.description
    
    # Verify guild members
    guild_db = await GuildRepository().get_by_id(guild.id)
    master_member = next(
        (member for member in guild_db["members"] if member.user_id == user_id),
        None
    )
    assert master_member is not None, "Master member not found in guild"
    assert master_member.role == MemberRole.MASTER.value
    
    # Verify member in database
    member_db = await MemberRepository().get_active_member_by_user_id(user_id)
    assert member_db is not None
    assert member_db["guild_id"] == guild.id
    assert member_db["role"] == MemberRole.MASTER.value

@pytest.mark.asyncio
async def test_create_duplicate_name():
    # Arrange
    user_id = "test-user-id"
    guild_name = "Test Guild"
    guild_data = GuildCreateRequestBody(
        name=guild_name,
        description="A test guild for testing"
    )
    
    # Create first guild
    await create_guild(guild_data, user_id)
    
    # Act & Assert
    with pytest.raises(DuplicateEntryError) as exc_info:
        await create_guild(guild_data, user_id)
    
    assert str(exc_info.value) == f"Guild with name {guild_data.name} already exists"