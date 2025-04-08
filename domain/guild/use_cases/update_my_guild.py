from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildUpdateRequestBody, GuildFlat
from infrastructure.error.error import ForbiddenError


# to avoid try update _sa_instance_state who isn t a real attribute of the model
def filter_sqlalchemy_internal_attributes(data: dict) -> dict:
    """Filtre les attributs internes de SQLAlchemy (comme _sa_instance_state)."""
    return {key: value for key, value in data.items() if not key.startswith('_sa_')}

async def update_my_guild(current_user_id: str, updates: GuildUpdateRequestBody) -> GuildFlat:
    repo = GuildRepository()

    guild = await repo.get_by_master_user_id(current_user_id)

    if not guild:
        raise ForbiddenError("Vous n'êtes maître d'aucune guilde.") 
    
    if updates.name is not None:
        guild.name = updates.name
    if updates.description is not None:
        guild.description = updates.description

    guild_data = filter_sqlalchemy_internal_attributes(guild.__dict__) 

    updated_guild = await repo.update(guild_data)
    return GuildFlat.model_validate(updated_guild)
