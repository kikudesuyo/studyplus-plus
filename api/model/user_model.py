from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    name: str
    studyplus_id: str
