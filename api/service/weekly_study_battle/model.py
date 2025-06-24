from pydantic import BaseModel

from api.model.user_model import UserModel


class PlaceModel(BaseModel):
    user: UserModel
    place: int
    total_duration: int


class StudyRecordModel(BaseModel):
    username: str
    nickname: str
    user_image_url: str
    duration: int
    record_datetime: str


class TotalStudyDurationModel(BaseModel):
    user: UserModel
    total_duration: int
