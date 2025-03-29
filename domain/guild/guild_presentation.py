from fastapi import APIRouter, Depends
from typing import Annotated

from domain.guild.guild_schema import GuildCreateRequestBody
from domain.guild.guild_domain import GuildDomain
from domain.user.user_schema import UserPrivate
from domain.auth.authentication_service import get_current_active_user
from domain.member.member_model import Member

router = APIRouter(prefix="/guild", tags=["guild"])


@router.post("")
async def create_guild_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    guild: GuildCreateRequestBody,
):
    guild = await GuildDomain().create(guild, current_user.id)
    return guild
