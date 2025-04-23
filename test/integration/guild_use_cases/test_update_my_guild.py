import pytest
import uuid
from domain.guild.use_cases.update_my_guild import update_my_guild
from domain.guild.use_cases.create_guild import create_guild
from domain.guild.guild_schema import GuildCreateRequestBody, GuildUpdateRequestBody
from domain.guild.guild_repository import GuildRepository
from domain.user.user_model import User
from domain.user.user_repository import UserRepository

@pytest.mark.asyncio
async def test_update_my_guild_success():
    # Arrange
    user_id = str(uuid.uuid4())
    username = "test-user"
    
    user = User(
        id=user_id,
        username=username,
        email=f"{username}@example.com",
        provider="test"
    )
    await UserRepository().save(user)

    guild_data = GuildCreateRequestBody(
        name="Original Guild",
        description="Initial description"
    )
    created_guild = await create_guild(guild_data, user_id)

    update_data = GuildUpdateRequestBody(
        name="Updated Guild Name",
        description="Updated description"
    )

    # Act
    updated = await update_my_guild(user_id, update_data)

    # Assert
    assert updated is not None
    assert updated.id == created_guild.id
    assert updated.description == "Updated description"

    # Vérifier dans la base de données
    stored = await GuildRepository().get_by_id(created_guild.id)
    assert stored['name'] == "Updated Guild Name"
    assert stored['description'] == "Updated description"
