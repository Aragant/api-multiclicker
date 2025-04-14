from sqlite3 import IntegrityError as SQLiteIntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from domain.guild.guild_model import Guild
from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildCreateRequestBody, GuildFlat
from domain.member.member_model import Member, MemberRole
from infrastructure.error.error import ConflictError


async def create_guild(newGuild: GuildCreateRequestBody, user_id: str) -> GuildFlat:
        try:
            guild = Guild(
                name=newGuild.name,
                description=newGuild.description,
                members=[Member(user_id=user_id, role=MemberRole.MASTER.value)],
            )
            created_guild = await GuildRepository().save(guild)
            return GuildFlat.model_validate(created_guild)
        except (SQLiteIntegrityError, SQLAlchemyIntegrityError) as e:
            # Vérifier si l'erreur est due à une contrainte d'unicité sur le nom de la guilde
            error_message = str(e)
            if "guild_name_key" in error_message or "UNIQUE constraint failed" in error_message:
                raise ConflictError(f"Une guilde avec le nom '{newGuild.name}' existe déjà.")
            raise e