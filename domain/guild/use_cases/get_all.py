from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildWithSumMembers


async def get_all() -> list[GuildWithSumMembers]:
        guilds = await GuildRepository().get_all()

        def setGuildMemberLength(guild):
            guild["sum_member"] = len(guild['members'])
            return GuildWithSumMembers.model_validate(guild)

        guildsWithMemberLength = map(
            setGuildMemberLength,
            guilds,
        )
        
        return guildsWithMemberLength