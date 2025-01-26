from pydantic import BaseModel


class UserFlat(BaseModel):
    username: str