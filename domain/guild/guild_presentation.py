from fastapi import APIRouter, Depends

from domain.guild.guild_schema import NewGuild
from domain.guild.guild_domain import GuildDomain

router = APIRouter(prefix="/guild", tags=["guild"])

@router.post("")
async def create_guild_route(guild: NewGuild):
    guild = await GuildDomain().create(guild)
    return guild
