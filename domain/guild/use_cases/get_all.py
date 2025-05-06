from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildWithSumMembers


async def get_all() -> list[GuildWithSumMembers]:
    guilds = await GuildRepository().get_all()
    return [
        GuildWithSumMembers.model_validate({**guild, "sum_member": len(guild["members"])})
        for guild in guilds
    ]