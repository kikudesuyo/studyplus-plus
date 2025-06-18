from typing import List, Optional

from pydantic import BaseModel


class BodyStudyRecord(BaseModel):
    event_id: int
    event_type: str
    username: str
    nickname: str
    badge_type: str
    user_image_url: Optional[str] = None
    like_count: int
    if_you_like: bool
    comment_count: int
    posted_at: str
    material_type: str
    material_code: str
    material_title: str
    material_image_url: str
    material_image_preset_name: Optional[str] = None
    record_id: int
    record_comment: str
    unit: str
    amount: int
    duration: int
    record_date: str
    record_datetime: str
    record_start: str
    images: List[str]
    tags: List[str]
    study_source_type: str


class Feed(BaseModel):
    feed_type: str
    body_study_record: Optional[BodyStudyRecord] = None


class FolloweeModel(BaseModel):
    current: str
    next: str
    feeds: List[Feed]
