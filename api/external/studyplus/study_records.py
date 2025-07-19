import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel, ConfigDict, Field

from api.external.studyplus.request_header import BASE_URL, get_auth_headers
from api.utils.api_error import ApiError


class StudyChallengePeriod(BaseModel):
    start_date: Optional[str]
    end_date: Optional[str]


class StudyChallenge(BaseModel):
    challenge_period: Optional[StudyChallengePeriod] = None
    challenge_duration: Optional[int] = None
    prev_duration: Optional[int] = None
    duration: Optional[int] = None
    prev_ratio: Optional[int] = None
    ratio: Optional[int] = None


class StudyRecordRes(BaseModel):
    record_id: int
    connection_result: Optional[Dict[str, Any]] = {}
    status: Optional[str] = ""
    study_challenge: Optional[StudyChallenge] = None


class StudyRecordReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    material_code: str = Field(..., alias="material_code")
    duration: int = Field(..., alias="duration")
    post_token: str = Field(..., alias="post_token")
    record_datetime: str = Field(..., alias="record_datetime")
    comment: Optional[str] = Field(None, alias="comment")
    runtimeType: str = Field(..., alias="runtimeType")
    study_source_type: str = Field(..., alias="study_source_type")


class StudyRecord:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = get_auth_headers(access_token)

    def _generate_post_token(self) -> str:
        """
        UUIDを生成して文字列形式で返します。
        例: "7160a019-d73b-483b-ad75-3f9e850ea9e6"
        """
        return str(uuid.uuid4())

    def _get_current_datetime_iso(self) -> str:
        """
        現在の日時をISO形式で返します。
        例: "2025-05-03T23:31:37.623+09:00"
        """
        now = datetime.now().astimezone()
        return now.isoformat()

    def post(
        self,
        material_code: str,
        duration: int,
        comment: Optional[str] = None,
        post_token: Optional[str] = None,
        record_datetime: Optional[str] = None,
    ) -> StudyRecordRes:
        """
        勉強記録を登録します。

        Args:
            material_code: 教材ID (教材なしの場合は""を指定)
            duration: 勉強時間（秒）
            comment: コメント（オプション）
            post_token: ポストトークン（UUIDで生成）
            record_datetime: 記録日時（指定されない場合は現在時刻）

        Returns:
            StudyRecordRes: APIレスポンス
        """
        if not post_token:
            post_token = self._generate_post_token()

        if not record_datetime:
            record_datetime = self._get_current_datetime_iso()

        req = StudyRecordReq(
            material_code=material_code,
            duration=duration,
            post_token=post_token,
            record_datetime=record_datetime,
            comment=comment,
            runtimeType="default",
            study_source_type="studyplus",
        )
        endpoint = f"{BASE_URL}/study_records"

        try:
            response = httpx.post(endpoint, json=req.model_dump(), headers=self.headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
            )
        return StudyRecordRes(**response.json())

    def put(
        self,
        record_id: int,
        material_code: str,
        duration: int,
        comment: Optional[str] = None,
        post_token: Optional[str] = None,
        record_datetime: Optional[str] = None,
    ) -> None:
        """勉強記録を更新する"""
        if not post_token:
            post_token = self._generate_post_token()
        if not record_datetime:
            record_datetime = self._get_current_datetime_iso()
        req = StudyRecordReq(
            material_code=material_code,
            duration=duration,
            post_token=post_token,
            record_datetime=record_datetime,
            comment=comment,
            runtimeType="default",
            study_source_type="studyplus",
        )

        endpoint = f"{BASE_URL}/study_records/{record_id}"
        try:
            response = httpx.put(endpoint, json=req.model_dump(), headers=self.headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ApiError(
                status_code=e.response.status_code,
                message=e.response.text,
                endpoint=endpoint,
            )
        except httpx.RequestError as e:
            raise ApiError(
                status_code=None,
                message=f"[External/Studyplus] Communication error: {str(e)}",
                endpoint=endpoint,
            )
