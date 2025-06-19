from typing import List, Optional

import requests
from pydantic import BaseModel, Field

from api.utils.http_utils import BASE_URL, ApiError, get_auth_headers


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


class FeedsReq(BaseModel):
    until: str = Field(..., alias="until")


class FeedsRes(BaseModel):
    current: str
    next: str
    feeds: List[Feed]


class TimelineFeeds:
    """フォロー中のユーザーの学習記録を取得するハンドラークラス"""

    def __init__(self, access_token: str):
        self.headers = get_auth_headers(access_token)

    def get_followee_study_feeds(self, until) -> FeedsRes:
        """フォロー中のユーザーの学習記録を取得する
        until: str
        フォーマット:
            "1748323851_2297584462" のような形式。
            最初の教材記録のID_最後の教材記録のID

        初回のリクエストではクエリパラメータは不要
        より過去の記録を取得したい場合は、前回のレスポンスに含まれる `next` の値を、
        次回のリクエストの `until` パラメータとして指定することで、続きの記録を取得できる。
        """
        req = FeedsReq(until=until)

        endpoint = f"{BASE_URL}/timeline_feeds/followee"
        params = req.model_dump(by_alias=True)

        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code == 200:
            return FeedsRes(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=endpoint,
                query=params,
            )

    def get_user_study_feeds(self, user_id, until) -> FeedsRes:
        """自分の学習記録を取得する
        until: str
        フォーマット:
            "1748323851_2297584462" のような形式。
            最初の教材記録のID_最後の教材記録のID

        初回のリクエストではクエリパラメータは不要
        より過去の記録を取得したい場合は、前回のレスポンスに含まれる `next` の値を、
        次回のリクエストの `until` パラメータとして指定することで、続きの記録を取得できる。
        """
        req = FeedsReq(until=until)

        endpoint = f"{BASE_URL}/timeline_feeds/user/{user_id}"
        params = req.model_dump(by_alias=True)

        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code == 200:
            return FeedsRes(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=endpoint,
                query=params,
            )
