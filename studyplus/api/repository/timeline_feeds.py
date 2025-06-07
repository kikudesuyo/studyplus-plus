from urllib.parse import urlencode

import requests
from pydantic import BaseModel, Field
from utils.http_utils import FOLLOWEE_ENDPOINT, ApiError, get_auth_headers

from studyplus.api.model.timeline_feeds_model import FolloweeModel


class FolloweeRepositoryReq(BaseModel):
    until: str = Field(..., alias="until")


class TimelineFeedsRepository:
    """フォロー中のユーザーの学習記録を取得するハンドラークラス"""

    def __init__(self, access_token: str):
        self.headers = get_auth_headers(access_token)

    def get_followee_study_records(self, until) -> FolloweeModel:
        """フォロー中のユーザーの学習記録を取得する
        until: str
        フォーマット:
            "1748323851_2297584462" のような形式。
            最初の教材記録のID_最後の教材記録のID

        初回のリクエストではクエリパラメータは不要
        より過去の記録を取得したい場合は、前回のレスポンスに含まれる `next` の値を、
        次回のリクエストの `until` パラメータとして指定することで、続きの記録を取得できる。
        """
        req = FolloweeRepositoryReq(until=until)
        url = f"{FOLLOWEE_ENDPOINT}?{urlencode(req.model_dump(by_alias=True))}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return FolloweeModel(**response.json())
        else:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
                endpoint=url,
            )
