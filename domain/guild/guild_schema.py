from pydantic import BaseModel

class NewGuild(BaseModel):
    name: str
    description: str
    owner_id: str

class GuildFlat(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str