from typing import Optional
from pydantic import BaseModel


class UserFlat(BaseModel):
    username: str
    disabled: bool
    
class UserPrivate(BaseModel):
    username: str
    
class UserForLogin(BaseModel):
    username: str
    password: str
    
class UserSignUp(BaseModel):
    username: str
    password: Optional[str] = None