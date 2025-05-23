from domain.guild.use_cases import (
    apply_guild,
    create_guild,
    get_all,
    get_guild_details,
    get_applicants_if_master,
    accept_applicant,
    reject_applicant,
)
from domain.member.member_schema import MemberApplicant
from fastapi import APIRouter, Depends
from typing import Annotated
from domain.guild.use_cases import update_my_guild
from domain.guild.guild_schema import (
    GuildCreateRequestBody,
    GuildFlat,
    GuildUpdateRequestBody,
    GuildWithSumMembers,
    GuildWithMembers,
)
from domain.user.user_schema import UserPrivate
from domain.auth.authentication_service import get_current_active_user
from fastapi import HTTPException

router = APIRouter(prefix="/guild", tags=["guild"])


@router.post("")
async def create_guild_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    guild: GuildCreateRequestBody,
):
    return await create_guild(guild, current_user.id)


@router.get("", response_model=list[GuildWithSumMembers])
async def get_all_guilds():
    return await get_all()


@router.post("/join/{guild_id}")
async def join_guild(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    guild_id: str,
):
    guild = await get_guild_details(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guilde non trouvée")
    return await apply_guild(current_user.id, guild_id)


@router.get("/applicants", response_model=list[MemberApplicant])
async def get_applicants(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
):
    return await get_applicants_if_master(current_user.id)


@router.patch("/accept/{applicant_id}")
async def accept_applicant_in_guild(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    applicant_id: str,
):
    return await accept_applicant(current_user.id, applicant_id)


@router.patch("/reject/{applicant_id}")
async def reject_applicant_in_guild(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    applicant_id: str,
):
    return await reject_applicant(current_user.id, applicant_id)


@router.get("/{guild_id}", response_model=GuildWithMembers)
async def get_guild_by_id(guild_id: str):
    guild = await get_guild_details(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guilde non trouvée")
    return guild


@router.patch("/me", response_model=GuildFlat)
async def patch_my_guild(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    updates: GuildUpdateRequestBody,
):
    return await update_my_guild(current_user.id, updates)
