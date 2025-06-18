from pydantic import BaseModel


class AuthModel(BaseModel):
    access_token: str
    refresh_token: str
    username: str
