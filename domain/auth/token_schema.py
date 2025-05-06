from pydantic import BaseModel
from domain.user.user_schema import UserPrivate

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenWithUser(Token):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserPrivate