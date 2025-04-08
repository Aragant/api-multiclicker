from domain.guild.use_cases import create, get_all, get_by_id
from fastapi import APIRouter, Depends
from typing import Annotated
from domain.guild.use_cases import update_my_guild
from domain.guild.guild_schema import GuildCreateRequestBody, GuildFlat, GuildUpdateRequestBody, GuildWithSumMembers, GuildWithMembers
from domain.user.user_schema import UserPrivate
from domain.auth.authentication_service import get_current_active_user
from fastapi import HTTPException

router = APIRouter(prefix="/guild", tags=["guild"])


@router.post("")
async def create_guild_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    guild: GuildCreateRequestBody,
):
    guild = await create(guild, current_user.id)
    return guild

@router.get("", response_model=list[GuildWithSumMembers])
async def get_all_guilds():
    return await get_all()

@router.get("/{guild_id}", response_model=GuildWithMembers)
async def get_guild_by_id(guild_id: str):
    guild = await get_by_id(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guilde non trouvée")
    return guild

@router.patch("/me", response_model=GuildFlat)
async def patch_my_guild(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    updates: GuildUpdateRequestBody,
):
    return await update_my_guild(current_user.id, updates)