from infrastructure.database.base_repository import BaseRepository
from domain.guild.guild_model import Guild

class GuildRepository():
    def __init__(self):
       self.repo = BaseRepository(Guild)

    async def save(self, guild: Guild):
        return await self.repo._save(guild)