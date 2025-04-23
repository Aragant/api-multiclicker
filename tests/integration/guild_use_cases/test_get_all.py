import pytest
from domain.guild.use_cases.get_all import get_all
from domain.guild.use_cases.create_guild import create_guild
from domain.guild.guild_schema import GuildCreateRequestBody
from domain.member.member_repository import MemberRepository

@pytest.mark.asyncio
async def test_get_all_success():
    # Arrange
    user_id1 = "test-user-id-1"
    user_id2 = "test-user-id-2"
    
    guild_data1 = GuildCreateRequestBody(
        name="Test Guild 1",
        description="First test guild"
    )
    
    guild_data2 = GuildCreateRequestBody(
        name="Test Guild 2",
        description="Second test guild"
    )
    
    # Create two guilds
    guild1 = await create_guild(guild_data1, user_id1)
    guild2 = await create_guild(guild_data2, user_id2)
    
    # Act
    guilds_map = await get_all()
    guilds = list(guilds_map)  # Convert map object to list
    
    # Assert
    assert len(guilds) >= 2, "Should return at least the two created guilds"
    
    # Verify guild names
    guild_names = [guild.name for guild in guilds]
    assert guild_data1.name in guild_names, "First guild should be in the list"
    assert guild_data2.name in guild_names, "Second guild should be in the list"
    
    # Verify sum_member field
    for guild in guilds:
        assert hasattr(guild, "sum_member"), "Each guild should have a sum_member field"
        assert guild.sum_member == 1, "Each guild should have exactly one member (the creator)"
    
    # Verify members in database
    member1 = await MemberRepository().get_active_member_by_user_id(user_id1)
    member2 = await MemberRepository().get_active_member_by_user_id(user_id2)
    
    assert member1 is not None and member1["guild_id"] == guild1.id, "First member should be associated with first guild"
    assert member2 is not None and member2["guild_id"] == guild2.id, "Second member should be associated with second guild" 