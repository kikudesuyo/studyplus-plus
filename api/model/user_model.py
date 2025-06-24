from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    studyplus_id: str
