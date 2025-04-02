from typing import Optional
from pydantic import BaseModel


class UserFlat(BaseModel):
    id: str
    username: str
    disabled: bool


class UserPrivate(BaseModel):
    id: str
    email: str
    username: Optional[str]
    disabled: bool
    description: Optional[str]
    
    
class UserPublic(BaseModel):
    id: str
    username: str
    description: Optional[str]


class UserForLogin(BaseModel):
    id: str
    username: str
    password: str


class UserSignUp(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: str


class UserUpdate(BaseModel):
    description: Optional[str]
