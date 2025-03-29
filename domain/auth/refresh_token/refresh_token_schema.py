from datetime import datetime

from pydantic import BaseModel


class RefreshTokenFlat(BaseModel):
    user_id: str
    refresh_token: str
    expires_at: datetime
    ip_address: str
    user_agent: str
