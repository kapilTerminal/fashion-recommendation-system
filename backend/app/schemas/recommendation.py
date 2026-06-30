from pydantic import BaseModel


class UserPreference(BaseModel):
    occasion: str
    style: str
    color: str