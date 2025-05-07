from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from infrastructure.error.error import ForbiddenError


class UserFlat(BaseModel):
    id: str
    username: str
    disabled: bool

class UserSignUp(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserPrivate(BaseModel):
    id: str
    email: str
    username: Optional[str]
    disabled: bool
    description: Optional[str]
    guild_id: Optional[str] = None
    
class UserPublic(BaseModel):
    id: str
    username: str
    description: Optional[str]


class UserForLogin(BaseModel):
    id: str
    username: str
    password: str

class UserSignUp(BaseModel):
    username: str
    password: str
    email: str
    
    @field_validator("email", mode="before")
    def validate_email(cls, v):
        try:
            EmailStr._validate(v)
        except ValueError:
            raise ForbiddenError("L'adresse email que vous avez fournie est invalide.")
        return v


class UserUpdate(BaseModel):
    description: Optional[str]
