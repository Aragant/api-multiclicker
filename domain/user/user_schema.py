from typing import Optional
from pydantic import BaseModel


class UserFlat(BaseModel):
    id: str
    username: str
    disabled: bool
    
class UserPrivate(BaseModel):
    id: str
    username: str
    disabled: bool
    description: Optional[str]
    
class UserForLogin(BaseModel):
    id: str
    username: str
    password: str
    
class UserSignUp(BaseModel):
    username: str
    password: Optional[str] = None
    
class UserUpdate(BaseModel):
    description: Optional[str]