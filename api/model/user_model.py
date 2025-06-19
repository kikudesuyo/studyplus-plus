from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    studyplus_id: str


class UserPlaceModel(BaseModel):
    user: UserModel
    place: int
    total_duration: int
