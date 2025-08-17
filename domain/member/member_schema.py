from pydantic import BaseModel


class MemberApplicant(BaseModel):
    id: str
    username: str
    user_id: str