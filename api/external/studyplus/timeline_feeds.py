from typing import List, Literal, Optional

import httpx
from pydantic import BaseModel, Field

from api.external.studyplus.request_header import BASE_URL, get_auth_headers
from api.utils.api_error import ApiError


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
    material_image_url: Optional[str] = None
    material_image_preset_name: Optional[str] = None
    record_id: int
    record_comment: str
    unit: str
    amount: int
    duration: int
    record_date: str
    record_datetime: str  # 2025-06-30T10:03:11Z # ISO 8601形式
    record_start: str
    images: List[str]
    tags: List[str]
    study_source_type: str


class Feed(BaseModel):
    feed_type: Literal["study_record", "study_challenge", "ads"]
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

        try:
            response = httpx.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
                query=params,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
            )
        return FeedsRes(**response.json())

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

        try:
            response = httpx.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
                query=params,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
            )
        return FeedsRes(**response.json())
