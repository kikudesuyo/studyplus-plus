from pydantic import BaseModel


class AuthModel(BaseModel):
    access_token: str
    refresh_token: str
    studyplus_user_id: str
