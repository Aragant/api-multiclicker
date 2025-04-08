from typing import Optional
from pydantic import BaseModel


class NewGuild(BaseModel):
    name: str
    description: str

class GuildCreateRequestBody(BaseModel):
    name: str
    description: str

class GuildUpdateRequestBody (BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None   

class GuildFlat(BaseModel):
    id: str
    name: str
    description: str

class GuildWithSumMembers(BaseModel):
    id: str
    name: str
    description: str
    sum_member: int
    
class GuildWithMembers(BaseModel):
    id: str
    name: str
    description: str
    sum_member: int
    members: list[str]
