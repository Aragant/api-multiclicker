import pytest
from domain.guild.use_cases.ask_join import ask_join
from domain.guild.use_cases.create import create
from domain.guild.guild_schema import GuildCreateRequestBody
from infrastructure.error.error import ForbiddenError
from domain.member.member_model import MemberRole
from domain.member.member_repository import MemberRepository
from domain.guild.guild_repository import GuildRepository

@pytest.mark.asyncio
async def test_ask_join_success(transaction):
    # Arrange
    master_user_id = "master-user-id"
    applicant_user_id = "applicant-user-id"
    
    # Créer une guilde avec un maître
    guild_data = GuildCreateRequestBody(
        name="Test Guild",
        description="A test guild for testing"
    )
    created_guild = await create(guild_data, master_user_id)
    
    # Vérifier que le maître est bien membre de la guilde
    master_member = await MemberRepository().get_active_member_by_user_id(master_user_id)
    assert master_member is not None
    assert master_member["guild_id"] == created_guild.id
    assert master_member["role"] == MemberRole.MASTER.value
    
    # Vérifier que l'applicant n'est pas déjà membre d'une guilde
    applicant_member = await MemberRepository().get_active_member_by_user_id(applicant_user_id)
    assert applicant_member is None
    
    # Act
    result = await ask_join(applicant_user_id, created_guild.id)
    
    # Assert
    assert result is not None
    assert result["user_id"] == applicant_user_id
    assert result["guild_id"] == created_guild.id
    assert result["role"] == MemberRole.APPLICANT.value
    
    # Vérifier que le membre a bien été ajouté à la base de données
    # Note: get_active_member_by_user_id ne retourne que les membres avec rôle MEMBER ou MASTER
    # Donc nous devons utiliser une autre méthode pour vérifier
    guild = await GuildRepository().get_by_id(created_guild.id)
    members = guild["members"]
    applicant_found = False
    for member in members:
        if member.user_id == applicant_user_id:
            applicant_found = True
            assert member.role == MemberRole.APPLICANT.value
            break
    assert applicant_found, "L'applicant n'a pas été trouvé dans les membres de la guilde"

@pytest.mark.asyncio
async def test_ask_join_already_in_guild(transaction):
    # Arrange
    master_user_id = "master-user-id"
    applicant_user_id = "applicant-user-id"
    
    # Créer deux guildes
    guild_data1 = GuildCreateRequestBody(
        name="Test Guild 1",
        description="A test guild for testing"
    )
    guild_data2 = GuildCreateRequestBody(
        name="Test Guild 2",
        description="Another test guild for testing"
    )
    
    guild1 = await create(guild_data1, master_user_id)
    guild2 = await create(guild_data2, applicant_user_id)
    
    # Vérifier que l'applicant est déjà membre d'une guilde
    applicant_member = await MemberRepository().get_active_member_by_user_id(applicant_user_id)
    assert applicant_member is not None
    assert applicant_member["guild_id"] == guild2.id
    assert applicant_member["role"] == MemberRole.MASTER.value
    
    # Act & Assert
    with pytest.raises(ForbiddenError, match="Vous ne pouvez pas rejoindre cette guilde."):
        await ask_join(applicant_user_id, guild1.id) 