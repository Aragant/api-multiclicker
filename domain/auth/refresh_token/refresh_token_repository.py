from domain.auth.refresh_token.refresh_token_model import RefreshToken
from datetime import datetime, timezone
from domain.auth.refresh_token.refresh_token_schema import RefreshTokenFlat
from infrastructure.database.base_repository import BaseRepository


class RefreshTokenRepository:
    def __init__(self):
        self.repo = BaseRepository(RefreshToken)

    async def save(self, instance: RefreshToken) -> RefreshToken:
        return await self.repo._save(instance)

    async def get_by_refresh_token(self, refresh_token: str) -> RefreshToken:
        refresh_token = await self.repo._get(refresh_token=refresh_token)
        refresh_token = RefreshTokenFlat.model_validate(refresh_token)
        if refresh_token is None:
            return None

        if refresh_token.expires_at < datetime.now(timezone.utc):
            return self.delete_by_refresh_token(refresh_token.refresh_token)

        return refresh_token

    async def delete_by_refresh_token(self, refresh_token: str) -> None:
        return await self.repo._delete(refresh_token=refresh_token)
