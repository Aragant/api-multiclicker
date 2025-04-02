from pydantic import BaseModel


class NewGuild(BaseModel):
    name: str
    description: str


class GuildCreateRequestBody(BaseModel):
    name: str
    description: str


class GuildFlat(BaseModel):
    id: str
    name: str
    description: str

class GuildWithMembers(BaseModel):
    id: str
    name: str
    description: str
    sum_member: int